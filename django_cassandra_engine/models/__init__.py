import logging
import inspect
import copy
import warnings
from operator import attrgetter
import collections
from functools import partial
from itertools import chain

import six
from django.conf import settings
from django.apps import apps
from django.core import validators
from django.db.models.base import ModelBase
from django.utils.translation import ugettext_lazy as _
from django.db.models import options

from ..compat import (BaseModel, ColumnDescriptor, ModelDefinitionException,
                      ModelException, ModelMetaClass, OrderedDict, columns,
                      query)
from .constants import ORDER_BY_WARN, ORDER_BY_ERROR_HELP, PK_META_MISSING_HELP
from . import django_field_methods
from . import django_model_methods


log = logging.getLogger(__name__)
_django_manager_attr_names = ('objects', 'default_manager', '_default_manager',
                              'base_manager', '_base_manager')


class DjangoCassandraOptions(options.Options):
    default_field_error_messages = {
        'invalid_choice': _('Value %(value)r is not a valid choice.'),
        'null': _('This field cannot be null.'),
        'blank': _('This field cannot be blank.'),
        'unique': _('%(model_name)s with this %(field_label)s '
                    'already exists.'),
        'unique_for_date': _("%(field_label)s must be unique for "
                             "%(date_field_label)s %(lookup_type)s."),
    }

    def __init__(self, *args, **kwargs):
        self.model_inst = kwargs.pop('cls')
        self._defined_columns = self.model_inst._defined_columns

        # Add Django attibutes to Columns
        self._give_columns_django_field_attributes()

        # Call Django to create _meta object
        super(DjangoCassandraOptions, self).__init__(*args, **kwargs)

        self._private_fields_name = 'private_fields'
        if hasattr(self, 'virtual_fields'):
            # Django < 1.10
            self._private_fields_name = 'virtual_fields'

        # Add Columns as Django Fields
        for column in six.itervalues(self._defined_columns):
            self.add_field(column)
        self.setup_pk()

        # Set further _meta attributes explicitly
        self.proxy_for_model = self.concrete_model = self.model_inst
        self.managed = False
        self.swappable = False

    def can_migrate(self, *args, **kwargs):
        return False

    def get_all_related_objects_with_model(self, *args, **kwargs):
        return []

    @property
    def related_objects(self):
        return []

    def setup_pk(self):
        self.pk = self.model_inst._get_explicit_pk_column()

    def add_field(self, field, **kwargs):
        """Add each field as a private field."""
        getattr(self, self._private_fields_name).append(field)
        self._expire_cache(reverse=True)
        self._expire_cache(reverse=False)

    def _get_fields(self, *args, **kwargs):
        fields = six.itervalues(self._defined_columns)
        return options.make_immutable_fields_list('get_fields()', fields)

    def _set_column_django_attributes(self, cql_column, name):
        allow_null = (
            (not cql_column.required and
             not cql_column.is_primary_key and
             not cql_column.partition_key) or cql_column.has_default and not cql_column.required
        )
        cql_column.error_messages = self.default_field_error_messages
        cql_column.empty_values = list(validators.EMPTY_VALUES)
        cql_column.db_index = cql_column.index
        cql_column.serialize = True
        cql_column.unique = cql_column.is_primary_key
        cql_column.hidden = False
        cql_column.auto_created = False
        cql_column.help_text = ''
        cql_column.blank = allow_null
        cql_column.null = allow_null
        cql_column.choices = []
        cql_column.flatchoices = []
        cql_column.validators = []
        cql_column.editable = True
        cql_column.concrete = True
        cql_column.many_to_many = False
        cql_column.many_to_one = False
        cql_column.one_to_many = False
        cql_column.one_to_one = False
        cql_column.is_relation = False
        cql_column.remote_field = None
        cql_column.unique_for_date = None
        cql_column.unique_for_month = None
        cql_column.unique_for_year = None
        cql_column.db_column = None
        cql_column.rel = None
        cql_column.attname = name
        cql_column.field = cql_column
        cql_column.model = self.model_inst
        cql_column.name = cql_column.db_field_name
        cql_column.verbose_name = cql_column.db_field_name
        cql_column._verbose_name = cql_column.db_field_name
        cql_column.field.related_query_name = lambda: None

    def _give_columns_django_field_attributes(self):
        """
        Add Django Field attributes to each cqlengine.Column instance.

        So that the Django Options class may interact with it as if it were
        a Django Field.
        """
        methods_to_add = (
            django_field_methods.value_from_object,
            django_field_methods.value_to_string,
            django_field_methods.get_attname,
            django_field_methods.get_cache_name,
            django_field_methods.pre_save,
            django_field_methods.get_prep_value,
            django_field_methods.get_choices,
            django_field_methods.get_choices_default,
            django_field_methods.save_form_data,
            django_field_methods.formfield,
            django_field_methods.get_db_prep_value,
            django_field_methods.get_db_prep_save,
            django_field_methods.db_type_suffix,
            django_field_methods.select_format,
            django_field_methods.get_internal_type,
            django_field_methods.get_attname_column,
            django_field_methods.check,
            django_field_methods._check_field_name,
            django_field_methods._check_db_index,
            django_field_methods.deconstruct,
            django_field_methods.run_validators,
            django_field_methods.clean,
            django_field_methods.get_db_converters,
            django_field_methods.get_prep_lookup,
            django_field_methods.get_db_prep_lookup,
            django_field_methods.get_filter_kwargs_for_object,
            django_field_methods.set_attributes_from_name,
            django_field_methods.db_parameters,
            django_field_methods.get_pk_value_on_save,
            django_field_methods.get_col,
        )
        for name, cql_column in six.iteritems(self._defined_columns):
            self._set_column_django_attributes(cql_column=cql_column, name=name)
            for method in methods_to_add:
                try:
                    method_name = method.func_name
                except AttributeError:
                    # python 3
                    method_name = method.__name__

                new_method = six.create_bound_method(method, cql_column)
                setattr(cql_column, method_name, new_method)


class DjangoCassandraModelMetaClass(ModelMetaClass, ModelBase):

    def __new__(cls, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, DjangoCassandraModelMetaClass)]

        if not parents:
            return super(ModelBase, cls).__new__(cls, name, bases, attrs)
        for attr in _django_manager_attr_names:
            setattr(cls, attr, None)

        # ################################################################
        # start code taken from python-driver 3.3.0 ModelMetaClass.__new__
        # ################################################################

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

        # TODO __default__ttl__ should be removed in the next major release
        options = attrs.get('__options__') or {}
        attrs['__default_ttl__'] = options.get('default_time_to_live')

        column_definitions = [(k, v) for k, v in attrs.items() if
                              isinstance(v, columns.Column)]
        column_definitions = sorted(column_definitions,
                                    key=lambda x: x[1].position)

        is_polymorphic_base = any(
            [c[1].discriminator_column for c in column_definitions])

        column_definitions = [x for x in
                              inherited_columns.items()] + column_definitions
        discriminator_columns = [c for c in column_definitions if
                                 c[1].discriminator_column]
        is_polymorphic = len(discriminator_columns) > 0
        if len(discriminator_columns) > 1:
            raise ModelDefinitionException(
                'only one discriminator_column can be defined in a model, {0} found'.format(
                    len(discriminator_columns)))

        if attrs['__discriminator_value__'] and not is_polymorphic:
            raise ModelDefinitionException(
                '__discriminator_value__ specified, but no base columns defined with discriminator_column=True')

        discriminator_column_name, discriminator_column = \
        discriminator_columns[0] if discriminator_columns else (None, None)

        if isinstance(discriminator_column,
                      (columns.BaseContainerColumn, columns.Counter)):
            raise ModelDefinitionException(
                'counter and container columns cannot be used as discriminator columns')

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
        if not is_abstract and not any(
                [v.primary_key for k, v in column_definitions]):
            raise ModelDefinitionException(
                "At least 1 primary key is required.")

        counter_columns = [c for c in defined_columns.values() if
                           isinstance(c, columns.Counter)]
        data_columns = [c for c in defined_columns.values() if
                        not c.primary_key and not isinstance(c,
                                                             columns.Counter)]
        if counter_columns and data_columns:
            raise ModelDefinitionException(
                'counter models may not have data columns')

        has_partition_keys = any(
            v.partition_key for (k, v) in column_definitions)

        def _transform_column(col_name, col_obj):
            column_dict[col_name] = col_obj
            if col_obj.primary_key:
                primary_keys[col_name] = col_obj
            col_obj.set_column_name(col_name)
            # set properties
            attrs[col_name] = ColumnDescriptor(col_obj)

        partition_key_index = 0
        # transform column definitions
        for k, v in column_definitions:
            # don't allow a column with the same name as a built-in attribute or method
            if k in BaseModel.__dict__:
                raise ModelDefinitionException(
                    "column '{0}' conflicts with built-in attribute/method".format(
                        k))

            # counter column primary keys are not allowed
            if (v.primary_key or v.partition_key) and isinstance(v,
                                                                 columns.Counter):
                raise ModelDefinitionException(
                    'counter columns cannot be used as primary keys')

            # this will mark the first primary key column as a partition
            # key, if one hasn't been set already
            if not has_partition_keys and v.primary_key:
                v.partition_key = True
                has_partition_keys = True
            if v.partition_key:
                v._partition_key_index = partition_key_index
                partition_key_index += 1

            overriding = column_dict.get(k)
            if overriding:
                v.position = overriding.position
                v.partition_key = overriding.partition_key
                v._partition_key_index = overriding._partition_key_index
            _transform_column(k, v)

        partition_keys = OrderedDict(
            k for k in primary_keys.items() if k[1].partition_key)
        clustering_keys = OrderedDict(
            k for k in primary_keys.items() if not k[1].partition_key)

        if attrs.get('__compute_routing_key__', True):
            key_cols = [c for c in partition_keys.values()]
            partition_key_index = dict(
                (col.db_field_name, col._partition_key_index) for col in
                key_cols)
            key_cql_types = [c.cql_type for c in key_cols]
            key_serializer = staticmethod(
                lambda parts, proto_version: [t.to_binary(p, proto_version) for
                                              t, p in
                                              zip(key_cql_types, parts)])
        else:
            partition_key_index = {}
            key_serializer = staticmethod(lambda parts, proto_version: None)

        # setup partition key shortcut
        if len(partition_keys) == 0:
            if not is_abstract:
                raise ModelException(
                    "at least one partition key must be defined")
        if len(partition_keys) == 1:
            pk_name = [x for x in partition_keys.keys()][0]
            attrs['pk'] = attrs[pk_name]
        else:
            # composite partition key case, get/set a tuple of values
            _get = lambda self: tuple(
                self._values[c].getval() for c in partition_keys.keys())
            _set = lambda self, val: tuple(
                self._values[c].setval(v) for (c, v) in
                zip(partition_keys.keys(), val))
            attrs['pk'] = property(_get, _set)

        # some validation
        col_names = set()
        for v in column_dict.values():
            # check for duplicate column names
            if v.db_field_name in col_names:
                raise ModelException(
                    "{0} defines the column '{1}' more than once".format(name,
                                                                         v.db_field_name))
            if v.clustering_order and not (
                v.primary_key and not v.partition_key):
                raise ModelException(
                    "clustering_order may be specified only for clustering primary keys")
            if v.clustering_order and v.clustering_order.lower() not in (
            'asc', 'desc'):
                raise ModelException(
                    "invalid clustering order '{0}' for column '{1}'".format(
                        repr(v.clustering_order), v.db_field_name))
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

        DoesNotExistBase = DoesNotExistBase or attrs.pop('DoesNotExist',
                                                         BaseModel.DoesNotExist)
        attrs['DoesNotExist'] = type('DoesNotExist', (DoesNotExistBase,), {})

        MultipleObjectsReturnedBase = None
        for base in bases:
            MultipleObjectsReturnedBase = getattr(base,
                                                  'MultipleObjectsReturned',
                                                  None)
            if MultipleObjectsReturnedBase is not None:
                break

        MultipleObjectsReturnedBase = MultipleObjectsReturnedBase or attrs.pop(
            'MultipleObjectsReturned', BaseModel.MultipleObjectsReturned)
        attrs['MultipleObjectsReturned'] = type('MultipleObjectsReturned',
                                                (MultipleObjectsReturnedBase,),
                                                {})

        # create the class and add a QuerySet to it
        klass = super(ModelBase, cls).__new__(cls, name, bases, attrs)

        udts = []
        for col in column_dict.values():
            columns.resolve_udts(col, udts)

        # for user_type in set(udts):
        #     user_type.register_for_keyspace(klass._get_keyspace())

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
        django_meta_default_names = options.DEFAULT_NAMES

        # patch django so Meta.get_pk_field can be specified these models
        options.DEFAULT_NAMES = django_meta_default_names + ('get_pk_field',)

        # We should call the contribute_to_class method only if it's bound
        if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            try:
                setattr(cls, name, value)
            except AttributeError:
                raise AttributeError('failed to set attribute {}'.format(name))
        options.DEFAULT_NAMES = django_meta_default_names

    @classmethod
    def _add_django_meta_and_register_model(cls, klass, attrs, name):
        # Create the class.
        module = attrs.get('__module__')
        if not module:
            return klass

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

        # Add _meta/Options attribute to the model
        new_class.add_to_class(
            '_meta', DjangoCassandraOptions(meta, app_label, cls=new_class))
        # Add manager to the model
        for manager_attr in _django_manager_attr_names:
            new_class.add_to_class(manager_attr, new_class.objects)
        # Register the model
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
        self.query = StubQuery(model=self.model)

    @property
    def objects(self):
        return self

    def first(self):
        return next(iter(self), None)

    def _clone(self):
        return copy.deepcopy(self)

    def all(self):
        return self

    def get_queryset(self):
        return self

    def count(self):
        return len(self)

    def exists(self):
        return len(self) > 0

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

    def exclude(self, *args, **kwargs):
        self._raise_not_implemented(method_name='defer')


class StubQuery(object):

    def __init__(self, model):
        self.model = model
        self.order_by = ['pk']

    @property
    def select_related(self):
        return False

    def add_context(self, *args, **kwargs):
        pass

    def get_context(self, *args, **kwargs):
        return {}

    def get_meta(self):
        return self.model._meta

    def _prepare(self, field):
        return self


class DjangoCassandraQuerySet(query.ModelQuerySet):
    name = 'objects'
    use_in_migrations = False

    def __init__(self, *args, **kwargs):
        super(query.ModelQuerySet, self).__init__(*args, **kwargs)
        self._allow_filtering = True
        self.query = StubQuery(model=self.model)

    def _select_fields(self):
        if self._defer_fields or self._only_fields:
            fields = self.model._columns.keys()
            if self._defer_fields:
                fields = [f for f in fields if f not in self._defer_fields]
            elif self._only_fields:
                fields = self._only_fields
            return [self.model._columns[f].db_field_name for f in fields]
        return super(query.ModelQuerySet, self)._select_fields()

    def count(self):
        if self._count is None:
            self._count = super(query.ModelQuerySet, self).count()
        return self._count

    def get_queryset(self):
        if len(self._where) > 0:
            return super(query.ModelQuerySet, self).filter()
        else:
            return super(query.ModelQuerySet, self).all()

    def exclude(self, *args, **kwargs):
        new_queryset = []
        for model in self.get_queryset():
            should_exclude_model = False
            for field_name, field_value in six.iteritems(kwargs):
                if getattr(model, field_name) == field_value:
                    should_exclude_model = True
                    break
            if not should_exclude_model:
                new_queryset.append(model)
        return ReadOnlyDjangoCassandraQuerySet(
            new_queryset, model_class=self.model)

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

    def exists(self):
        return self.count() > 0

    def get(self, *args, **kwargs):
        obj = super(DjangoCassandraQuerySet, self).get(*args, **kwargs)
        obj.pk = getattr(obj, obj._get_explicit_pk_column().name)
        return obj

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
                    order_using_python = settings.CASSANDRA_FALLBACK_ORDER_BY_PYTHON
                    if order_using_python:
                        log.debug('ordering in python column "%s"', col)
                        msg = ORDER_BY_WARN.format(col=col, exc=exc)
                        warnings.warn(msg)
                    else:
                        raise query.QueryException(
                            '{exc}\n\n'
                            '{help}'.format(exc=exc, help=ORDER_BY_ERROR_HELP))
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

    def _clone(self):
        return copy.deepcopy(self)


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

    def __init__(self, *args, **kwargs):
        super(DjangoCassandraModel, self).__init__(*args, **kwargs)
        methods = inspect.getmembers(django_model_methods, inspect.isfunction)
        for method_name, method in methods:
            new_method = partial(method, self)
            setattr(self, method_name, new_method)

    def __hash__(self):
        if self._get_pk_val() is None:
            raise TypeError("Model instances without primary key value are unhashable")
        return hash(self._get_pk_val())

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
        return tuple(c for c in six.itervalues(cls._columns)
                     if c.is_primary_key is True)

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
            return cls._meta.get_field(cls._meta.pk.name)
        return cls._columns[name]

    @classmethod
    def _get_explicit_pk_column(cls):
        try:
            if len(cls._primary_keys) > 1:
                try:
                    pk_field = cls.Meta.get_pk_field
                except AttributeError:
                    raise RuntimeError(PK_META_MISSING_HELP.format(cls))
                return cls._primary_keys[pk_field]
            else:
                return list(six.itervalues(cls._primary_keys))[0]
        except IndexError:
            return None
