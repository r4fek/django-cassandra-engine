import logging
import inspect
import copy
import warnings
from operator import attrgetter
import collections
from itertools import chain

import six
from django.conf import settings
from django.apps import apps
from django.db.models.base import ModelBase
from django.db.models.options import Options
import cassandra
from cassandra.cqlengine import query
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import (
    ModelMetaClass, ModelException, ColumnDescriptor, BaseModel,
    ModelDefinitionException
)
from cassandra.util import OrderedDict

from .constants import (
    ORDER_BY_WARN,
    ORDER_BY_ERROR_HELP,
    CASSANDRA_DRIVER_COMPAT_VERSIONS
)


log = logging.getLogger(__name__)
USE_FALLBACK_ORDER_BY = getattr(
    settings, 'CASSANDRA_FALLBACK_ORDER_BY_PYTHON', False)
if cassandra.__version__ not in CASSANDRA_DRIVER_COMPAT_VERSIONS:
    raise RuntimeError(
        'Django Cassandra Models require cassandra-driver versions {} '
        'Version "{}" found'.format(CASSANDRA_DRIVER_COMPAT_VERSIONS,
                                    cassandra.__version__))


class DjangoCassandraOptions(Options):

    def __init__(self, *args, **kwargs):
        self.model_inst = kwargs.pop('cls')
        self._defined_columns = self.model_inst.__dict__['_defined_columns']

        # Add Django attibutes to Columns
        self._give_column_django_field_attributes()

        # Call Django to create _meta object
        super(DjangoCassandraOptions, self).__init__(*args, **kwargs)

        # Add Columns as Django Fields
        for column in self._defined_columns.values():
            self.add_field(column)

        # Set further _meta attributes explicitly
        self.proxy_for_model = self.concrete_model = self.model_inst
        self.pk = self._get_first_primary_key_column
        self.managed = False
        self.swappable = False

    def can_migrate(self, *args, **kwargs):
        return False

    def get_all_related_objects_with_model(self, *args, **kwargs):
        return []

    @property
    def related_objects(self):
        return []

    def add_field(self, field):
        """Add each field as a virtual_field."""
        self.virtual_fields.append(field)
        self.setup_pk(field)
        self._expire_cache(reverse=True)
        self._expire_cache(reverse=False)

    def _get_fields(self, *args, **kwargs):
        return self._defined_columns.values()

    @property
    def _get_first_primary_key_column(self):
        try:
            return list(self.model_inst._primary_keys.values())[0]
        except IndexError:
            return None

    def _give_column_django_field_attributes(self):
        """
        Add Django Field attributes to each cqlengine.Column instance.

        So that the Django Options class may interact with it as if it were
        a Django Field.
        """
        for name, cql_column in self._defined_columns.items():
            cql_column.serialize = not cql_column.is_primary_key
            cql_column.hidden = False
            cql_column.auto_created = False
            cql_column.help_text = ''
            cql_column.blank = not cql_column.required
            cql_column.null = not cql_column.required
            cql_column.choices = []
            cql_column.editable = True
            cql_column.many_to_many = False
            cql_column.many_to_one = False
            cql_column.one_to_many = False
            cql_column.one_to_one = False
            cql_column.is_relation = False
            cql_column.remote_field = None
            cql_column.unique_for_date = None
            cql_column.unique_for_month = None
            cql_column.unique_for_year = None
            cql_column.rel = None
            cql_column.attname = name
            cql_column.field = cql_column
            cql_column.model = self.model_inst
            cql_column.name = cql_column.db_field_name
            cql_column.verbose_name = cql_column.db_field_name
            cql_column._verbose_name = cql_column.db_field_name
            cql_column.field.related_query_name = lambda: None


class DjangoCassandraModelMetaClass(ModelMetaClass, ModelBase):

    def __new__(cls, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, DjangoCassandraModelMetaClass)]
        if not parents:
            return super(ModelBase, cls).__new__(cls, name, bases, attrs)

        # ################################################################
        # start code taken from python-driver 3.3.0 ModelMetaClass.__new__
        # ################################################################

        # move column definitions into columns dict
        # and set default column names
        column_dict = OrderedDict()
        primary_keys = OrderedDict()
        pk_name = None

        # get inherited properties
        inherited_columns = OrderedDict()
        for base in bases:
            for k, v in getattr(base, '_defined_columns', {}).items():
                inherited_columns.setdefault(k, v)

        # short circuit __abstract__ inheritance
        is_abstract = attrs['__abstract__'] = attrs.get('__abstract__', False)

        # short circuit __discriminator_value__ inheritance
        attrs['__discriminator_value__'] = attrs.get('__discriminator_value__')

        options = attrs.get('__options__') or {}
        attrs['__default_ttl__'] = options.get('default_time_to_live')

        def _transform_column(col_name, col_obj):
            column_dict[col_name] = col_obj
            if col_obj.primary_key:
                primary_keys[col_name] = col_obj
            col_obj.set_column_name(col_name)
            # set properties
            attrs[col_name] = ColumnDescriptor(col_obj)

        column_definitions = [(k, v) for k, v in attrs.items() if isinstance(v, columns.Column)]
        column_definitions = sorted(column_definitions, key=lambda x: x[1].position)

        is_polymorphic_base = any([c[1].discriminator_column for c in column_definitions])

        column_definitions = [x for x in inherited_columns.items()] + column_definitions
        discriminator_columns = [c for c in column_definitions if c[1].discriminator_column]
        is_polymorphic = len(discriminator_columns) > 0
        if len(discriminator_columns) > 1:
            raise ModelDefinitionException('only one discriminator_column can be defined in a model, {0} found'.format(len(discriminator_columns)))

        if attrs['__discriminator_value__'] and not is_polymorphic:
            raise ModelDefinitionException('__discriminator_value__ specified, but no base columns defined with discriminator_column=True')

        discriminator_column_name, discriminator_column = discriminator_columns[0] if discriminator_columns else (None, None)

        if isinstance(discriminator_column, (columns.BaseContainerColumn, columns.Counter)):
            raise ModelDefinitionException('counter and container columns cannot be used as discriminator columns')

        # find polymorphic base class
        polymorphic_base = None
        if is_polymorphic and not is_polymorphic_base:
            def _get_polymorphic_base(bases):
                for base in bases:
                    if getattr(base, '_is_polymorphic_base', False):
                        return base
                    klass = _get_polymorphic_base(base.__bases__)
                    if klass:
                        return klass
            polymorphic_base = _get_polymorphic_base(bases)

        defined_columns = OrderedDict(column_definitions)

        # check for primary key
        if not is_abstract and not any([v.primary_key for k, v in column_definitions]):
            raise ModelDefinitionException("At least 1 primary key is required.")

        counter_columns = [c for c in defined_columns.values() if isinstance(c, columns.Counter)]
        data_columns = [c for c in defined_columns.values() if not c.primary_key and not isinstance(c, columns.Counter)]
        if counter_columns and data_columns:
            raise ModelDefinitionException('counter models may not have data columns')

        has_partition_keys = any(v.partition_key for (k, v) in column_definitions)

        partition_key_index = 0
        # transform column definitions
        for k, v in column_definitions:
            # don't allow a column with the same name as a built-in attribute or method
            if k in BaseModel.__dict__:
                raise ModelDefinitionException("column '{0}' conflicts with built-in attribute/method".format(k))

            # counter column primary keys are not allowed
            if (v.primary_key or v.partition_key) and isinstance(v, columns.Counter):
                raise ModelDefinitionException('counter columns cannot be used as primary keys')

            # this will mark the first primary key column as a partition
            # key, if one hasn't been set already
            if not has_partition_keys and v.primary_key:
                v.partition_key = True
                has_partition_keys = True
            if v.partition_key:
                v._partition_key_index = partition_key_index
                partition_key_index += 1
            _transform_column(k, v)

        partition_keys = OrderedDict(k for k in primary_keys.items() if k[1].partition_key)
        clustering_keys = OrderedDict(k for k in primary_keys.items() if not k[1].partition_key)

        if attrs.get('__compute_routing_key__', True):
            key_cols = [c for c in partition_keys.values()]
            partition_key_index = dict((col.db_field_name, col._partition_key_index) for col in key_cols)
            key_cql_types = [c.cql_type for c in key_cols]
            key_serializer = staticmethod(lambda parts, proto_version: [t.to_binary(p, proto_version) for t, p in zip(key_cql_types, parts)])
        else:
            partition_key_index = {}
            key_serializer = staticmethod(lambda parts, proto_version: None)

        # setup partition key shortcut
        if len(partition_keys) == 0:
            if not is_abstract:
                raise ModelException("at least one partition key must be defined")
        if len(partition_keys) == 1:
            pk_name = [x for x in partition_keys.keys()][0]
            attrs['pk'] = attrs[pk_name]
        else:
            # composite partition key case, get/set a tuple of values
            _get = lambda self: tuple(self._values[c].getval() for c in partition_keys.keys())
            _set = lambda self, val: tuple(self._values[c].setval(v) for (c, v) in zip(partition_keys.keys(), val))
            attrs['pk'] = property(_get, _set)

        # some validation
        col_names = set()
        for v in column_dict.values():
            # check for duplicate column names
            if v.db_field_name in col_names:
                raise ModelException("{0} defines the column '{1}' more than once".format(name, v.db_field_name))
            if v.clustering_order and not (v.primary_key and not v.partition_key):
                raise ModelException("clustering_order may be specified only for clustering primary keys")
            if v.clustering_order and v.clustering_order.lower() not in ('asc', 'desc'):
                raise ModelException("invalid clustering order '{0}' for column '{1}'".format(repr(v.clustering_order), v.db_field_name))
            col_names.add(v.db_field_name)

        # create db_name -> model name map for loading
        db_map = {}
        for col_name, field in column_dict.items():
            db_field = field.db_field_name
            if db_field != col_name:
                db_map[db_field] = col_name

        # add management members to the class
        attrs['_columns'] = column_dict
        attrs['_primary_keys'] = primary_keys
        attrs['_defined_columns'] = defined_columns

        # maps the database field to the models key
        attrs['_db_map'] = db_map
        attrs['_pk_name'] = pk_name
        attrs['_dynamic_columns'] = {}

        attrs['_partition_keys'] = partition_keys
        attrs['_partition_key_index'] = partition_key_index
        attrs['_key_serializer'] = key_serializer
        attrs['_clustering_keys'] = clustering_keys
        attrs['_has_counter'] = len(counter_columns) > 0

        # add polymorphic management attributes
        attrs['_is_polymorphic_base'] = is_polymorphic_base
        attrs['_is_polymorphic'] = is_polymorphic
        attrs['_polymorphic_base'] = polymorphic_base
        attrs['_discriminator_column'] = discriminator_column
        attrs['_discriminator_column_name'] = discriminator_column_name
        attrs['_discriminator_map'] = {} if is_polymorphic_base else None

        # setup class exceptions
        DoesNotExistBase = None
        for base in bases:
            DoesNotExistBase = getattr(base, 'DoesNotExist', None)
            if DoesNotExistBase is not None:
                break

        DoesNotExistBase = DoesNotExistBase or attrs.pop('DoesNotExist', BaseModel.DoesNotExist)
        attrs['DoesNotExist'] = type('DoesNotExist', (DoesNotExistBase,), {})

        MultipleObjectsReturnedBase = None
        for base in bases:
            MultipleObjectsReturnedBase = getattr(base, 'MultipleObjectsReturned', None)
            if MultipleObjectsReturnedBase is not None:
                break

        MultipleObjectsReturnedBase = MultipleObjectsReturnedBase or attrs.pop('MultipleObjectsReturned', BaseModel.MultipleObjectsReturned)
        attrs['MultipleObjectsReturned'] = type('MultipleObjectsReturned', (MultipleObjectsReturnedBase,), {})

        # create the class and add a QuerySet to it
        klass = super(ModelBase, cls).__new__(cls, name, bases, attrs)

        udts = []
        for col in column_dict.values():
            columns.resolve_udts(col, udts)

        for user_type in set(udts):
            user_type.register_for_keyspace(klass._get_keyspace())

        # ################################################################
        # end code taken from python-driver 3.3.0 ModelMetaClass.__new__
        # ################################################################

        klass._deferred = False
        if not is_abstract:
            klass = cls._add_django_meta_and_register_model(
                klass=klass,
                attrs=attrs,
                name=name
            )
        return klass

    def add_to_class(cls, name, value):
        # We should call the contribute_to_class method only if it's bound
        if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

    @classmethod
    def _add_django_meta_and_register_model(cls, klass, attrs, name):
        # Create the class.
        module = attrs.pop('__module__')
        new_class = klass
        attr_meta = attrs.pop('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta

        if meta:
            meta.managed = False

        app_label = None

        # Look for an application configuration to attach the model to.
        app_config = apps.get_containing_app_config(module)

        if getattr(meta, 'app_label', None) is None:
            if app_config is None:
                if not abstract:
                    raise RuntimeError(
                        "Model class %s.%s doesn't declare an explicit "
                        "app_label and isn't in an application in "
                        "INSTALLED_APPS." % (module, name)
                    )

            else:
                app_label = app_config.label

        new_class.add_to_class(
            '_meta', DjangoCassandraOptions(meta, app_label, cls=new_class))
        new_class.add_to_class('_default_manager', new_class.objects)
        new_class.add_to_class('_base_manager', new_class.objects)
        new_class._meta.apps.register_model(new_class._meta.app_label, new_class)
        return new_class

    @classmethod
    def check(cls, **kwargs):
        errors = []
        return errors


def convert_pk_field_names_to_real(model, field_names):
    """
    Convert field names including 'pk' to the real field names:

    >>> convert_pk_field_names_to_real(['pk', 'another_field'])
    ['real_pk_field', 'another_field']
    """
    pk_field_names = tuple(f.name for f in model._get_primary_key_columns())

    def append_field(field_name):
        if field_name not in real_field_names:
            real_field_names.append(field_name)

    real_field_names = []
    for name in field_names:
        if name == 'pk':
            for real_pk_field_name in pk_field_names:
                append_field(real_pk_field_name)
        elif name == '-pk':
            for real_pk_field_name in pk_field_names:
                append_field('-' + real_pk_field_name)
        else:
            append_field(name)
    return real_field_names


class ReadOnlyDjangoCassandraQuerySet(list):
    name = 'objects'
    use_in_migrations = False

    def __init__(self, data, model_class):
        if not isinstance(data, collections.Iterable):
            raise TypeError(
                'ReadOnlyDjangoCassandraQuerySet requires iterable data')
        super(ReadOnlyDjangoCassandraQuerySet, self).__init__(data)
        self.model = model_class

    @property
    def objects(self):
        return self

    def first(self):
        return next(iter(self), None)

    def all(self):
        return self

    def count(self):
        return len(self)

    def values_list(self, *fields, **kwargs):
        fields = convert_pk_field_names_to_real(model=self.model,
                                                field_names=fields)

        values_list = []
        for model_record in self:
            values_list_item = []
            for field_name in fields:
                values_list_item.append(model_record[field_name])
            values_list.append(values_list_item)

        if kwargs.get('flat') is True:
            values_list = list(chain.from_iterable(values_list))
        return values_list

    def _raise_not_implemented(self, method_name):
        raise NotImplementedError(
            'You cannot .{}() on a DjangoCassandraQuerySet which '
            'has been ordered using python'.format(method_name)
        )

    def filter(self, **kwargs):
        self._raise_not_implemented(method_name='filter')

    def get(self, **kwargs):
        self._raise_not_implemented(method_name='get')

    def distinct(self, *args, **kwargs):
        self._raise_not_implemented(method_name='distinct')

    def limit(self, *args, **kwargs):
        self._raise_not_implemented(method_name='limit')

    def only(self, *args, **kwargs):
        self._raise_not_implemented(method_name='only')

    def create(self, *args, **kwargs):
        self._raise_not_implemented(method_name='create')

    def delete(self, *args, **kwargs):
        self._raise_not_implemented(method_name='delete')

    def defer(self, *args, **kwargs):
        self._raise_not_implemented(method_name='defer')


class DjangoCassandraQuerySet(query.ModelQuerySet):
    name = 'objects'
    use_in_migrations = False
    _USE_FALLBACK_ORDER_BY = USE_FALLBACK_ORDER_BY

    def python_order_by(self, qset, colnames):
        if not isinstance(qset, list):
            raise TypeError('qset must be a list')

        colnames = convert_pk_field_names_to_real(model=self.model,
                                                  field_names=colnames)

        any_cols_revesed = any(c.startswith('-') for c in colnames)
        if any_cols_revesed:
            for col in colnames:
                should_reverse = col.startswith('-')
                if should_reverse:
                    col = col[1:]

                qset.sort(key=attrgetter(col), reverse=should_reverse)
        else:
            new_colnames = []
            for col in colnames:
                if col == 'pk':
                    pk_cols = self.model._get_primary_key_column_names()
                    for pk_name in pk_cols:
                        new_colnames.append(pk_name)
                else:
                    new_colnames.append(col)
            try:
                qset.sort(key=attrgetter(*new_colnames))
            except AttributeError:
                msg = 'Can\'t resolve one of column names: {}'.format(
                    *new_colnames)
                raise query.QueryException(msg)

        return ReadOnlyDjangoCassandraQuerySet(qset, model_class=self.model)

    def order_by(self, *colnames):
        if len(colnames) == 0:
            clone = copy.deepcopy(self)
            clone._order = []
            return clone

        order_using_python = False
        conditions = []
        for col in colnames:
            try:
                conditions.append('"{0}" {1}'.format(
                    *self._get_ordering_condition(col))
                )
            except query.QueryException as exc:
                order_by_exception = (
                    'Can\'t order' in str(exc) or
                    'Can\'t resolve the column name' in str(exc)
                )

                if order_by_exception:
                    order_using_python = self._USE_FALLBACK_ORDER_BY
                    if order_using_python:
                        log.debug('ordering in python column "%s"', col)
                        msg = ORDER_BY_WARN.format(col=col, exc=exc)
                        warnings.warn(msg)
                    else:
                        raise query.QueryException(
                            '{exc}\n\n'
                            '{help}'.format(exc=exc, help=ORDER_BY_ERROR_HELP)
                        )
                else:
                    raise exc

        clone = copy.deepcopy(self)

        if order_using_python is True:
            return self.python_order_by(qset=list(clone), colnames=colnames)
        else:
            clone._order.extend(conditions)
            return clone

    def values_list(self, *fields, **kwargs):
        if 'pk' in fields:
            fields = convert_pk_field_names_to_real(
                model=self.model, field_names=fields)

        super_values_list = super(DjangoCassandraQuerySet, self).values_list
        return super_values_list(*fields, **kwargs)


class DjangoCassandraModel(
    six.with_metaclass(DjangoCassandraModelMetaClass, BaseModel)
):
    __queryset__ = DjangoCassandraQuerySet
    __abstract__ = True
    __table_name__ = None
    __table_name_case_sensitive__ = False
    __keyspace__ = None
    __options__ = None

    __discriminator_value__ = None
    __compute_routing_key__ = True

    @classmethod
    def get(cls, *args, **kwargs):
        raise AttributeError('model has no attribute \'get\'')

    @classmethod
    def filter(cls, *args, **kwargs):
        raise AttributeError('model has no attribute \'filter\'')

    @classmethod
    def all(cls, *args, **kwargs):
        raise AttributeError('model has no attribute \'all\'')

    @classmethod
    def _get_primary_key_columns(cls):
        return tuple(
            c for c in cls._columns.values() if c.is_primary_key is True)

    @classmethod
    def _get_primary_key_column_names(cls):
        return tuple(c.name for c in cls._get_primary_key_columns())

    @classmethod
    def _get_column(cls, name):
        """
        Based on cqlengine.models.BaseModel._get_column.

        But to work with 'pk'
        """
        if name == 'pk':
            first_primary_column = cls._get_primary_key_columns()[0]
            return first_primary_column
        return cls._columns[name]
