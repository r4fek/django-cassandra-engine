from datetime import datetime
from unittest import skipIf
import copy
import uuid

from cassandra.cqlengine import ValidationError as CQLValidationError
from django.core import validators
from django.forms import fields

from common.models import CassandraFamilyMember
from django_cassandra_engine.test import TestCase as CassandraTestCase


class TestDjangoCassandraModel(CassandraTestCase):
    def setUp(self):
        self.some_uuid = uuid.uuid4()
        self.family_member = CassandraFamilyMember.objects.create(
            id=self.some_uuid,
            first_name="Homer",
            last_name="Simpson",
            is_real=False,
            favourite_number=666,
            favourite_float_number=43.4,
            created_on=datetime.now(),
        )

    def test_model_is_hashable(self):
        models = set()
        models.add(self.family_member)
        self.assertEqual(1, len(models))

    def test_serializable_value(self):
        self.assertEqual(self.some_uuid, self.family_member.serializable_value("id"))
        self.assertEqual(
            self.family_member.first_name,
            self.family_member.serializable_value("first_name"),
        )

    def test_clone_queryset(self):
        qset = CassandraFamilyMember.objects.filter(id=self.some_uuid)
        self.assertNotEqual(id(qset._clone()), id(qset))

    def test_create(self):
        family_member = self.family_member
        self.assertEqual(family_member.first_name, "Homer")
        self.assertEqual(family_member.last_name, "Simpson")
        self.assertEqual(family_member.is_real, False)
        self.assertEqual(family_member.favourite_number, 666)
        self.assertEqual(family_member.favourite_float_number, 43.4)

    def test_get_by_pk(self):
        got_family_member = CassandraFamilyMember.objects.allow_filtering().get(
            pk=self.family_member.id
        )
        self.assertIsNotNone(got_family_member)

    def test_exclude(self):
        results = CassandraFamilyMember.objects.exclude(id=self.some_uuid)
        for model in results:
            self.assertNotEqual(model.id, self.some_uuid)

    def test_exclude_after_filter(self):
        results = CassandraFamilyMember.objects.filter(id=self.some_uuid).exclude(
            last_name="Simpson"
        )
        self.assertEqual(len(results), 0)

    def test_exclude_after_all(self):
        keeper = CassandraFamilyMember.objects.create(
            id=uuid.uuid4(),
            first_name="Ned",
            last_name="Flanders",
            is_real=False,
            favourite_number=666,
            favourite_float_number=43.4,
            created_on=datetime.now(),
        )
        results = CassandraFamilyMember.objects.all().exclude(last_name="Simpson")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, keeper.id)

    def test_get_by_pk_returns_primary_key_instead_of_partition_key(self):
        got_family_member = CassandraFamilyMember.objects.allow_filtering().get(
            pk=self.family_member.id
        )

        self.assertEqual(got_family_member.pk, self.family_member.id)

    def test_default_manager_is_set(self):
        self.assertTrue(
            isinstance(
                CassandraFamilyMember._default_manager,
                type(CassandraFamilyMember.objects),
            )
        )
        self.assertTrue(
            isinstance(
                CassandraFamilyMember._base_manager,
                type(CassandraFamilyMember.objects),
            )
        )
        self.assertTrue(hasattr(CassandraFamilyMember._default_manager, "all"))
        self.assertTrue(hasattr(CassandraFamilyMember._default_manager, "filter"))

    def test_get_queryset(self):
        results = CassandraFamilyMember.objects.get_queryset()
        self.assertTrue(results[0].id, self.some_uuid)

    def test_calling_queryset_methods_not_through_manager_raises(self):
        with self.assertRaises(AttributeError):
            CassandraFamilyMember.all()

        with self.assertRaises(AttributeError):
            CassandraFamilyMember.get()

        with self.assertRaises(AttributeError):
            CassandraFamilyMember.filter()

    def test_manager_has_a_name(self):
        self.assertEqual(CassandraFamilyMember._default_manager.name, "objects")

    def test_can_migrate(self):
        self.assertFalse(CassandraFamilyMember._meta.can_migrate(connection=None))

    def test_get_all_related_objects_with_model(self):
        self.assertEqual(
            CassandraFamilyMember._meta.get_all_related_objects_with_model(),
            [],
        )

    def test_related_objects_property(self):
        self.assertEqual(CassandraFamilyMember._meta.related_objects, [])

    def test_db_table(self):
        self.assertEqual(
            CassandraFamilyMember._meta.db_table,
            "common_cassandrafamilymember",
        )

    def test_pk_attribute(self):
        self.assertEqual(
            CassandraFamilyMember._meta.pk,
            CassandraFamilyMember._meta.get_field("id"),
        )

    def test_get_fields(self):
        expected_field_names = [
            "id",
            "first_name",
            "last_name",
            "is_real",
            "favourite_number",
            "favourite_float_number",
            "created_on",
        ]
        fields = CassandraFamilyMember._meta._get_fields()
        self.assertEqual(len(fields), len(expected_field_names))
        self.assertEqual([f.name for f in fields], expected_field_names)

    def test_meta_attrs(self):
        self.assertEqual(
            CassandraFamilyMember._meta.model_name, "cassandrafamilymember"
        )
        self.assertEqual(CassandraFamilyMember._meta.swappable, False)
        self.assertEqual(CassandraFamilyMember._meta.managed, False)

    def test_values_list_with_id_pk_field_returns_it(self):
        all_things = CassandraFamilyMember.objects.allow_filtering().filter(
            id=self.some_uuid
        )

        self.assertEqual(
            list(all_things.values_list("id", flat=True)), [self.some_uuid]
        )

    def test_values_list_with_pk_returns_the_primary_key_field_uuid(self):
        all_things = CassandraFamilyMember.objects.allow_filtering().filter(
            id=self.some_uuid
        )

        model = all_things[0]

        self.assertEqual(
            list(all_things.values_list("pk")),
            [
                [
                    model.id,
                    model.first_name,
                    model.last_name,
                    model.favourite_float_number,
                ]
            ],
        )

    def test_values_list_with_pk_can_return_multiple_pks(self):
        some_uuid = uuid.uuid4()

        family_member = CassandraFamilyMember.objects.create(
            id=some_uuid,
            first_name="Homer",
            last_name="Simpson",
            is_real=False,
            favourite_number=666,
            favourite_float_number=43.4,
            created_on=datetime.now(),
        )

        all_things = CassandraFamilyMember.objects.allow_filtering().filter(
            id=some_uuid
        )

        expected = [
            [
                family_member.id,
                family_member.first_name,
                family_member.last_name,
                family_member.favourite_float_number,
            ]
        ]
        self.assertEqual(len(all_things.values_list("pk")), len(expected))

    def test_private_fields_are_set(self):
        private_fields = [f.name for f in CassandraFamilyMember._meta.private_fields]
        expected_private_fields = [
            "id",
            "first_name",
            "last_name",
            "is_real",
            "favourite_number",
            "favourite_float_number",
            "created_on",
        ]
        self.assertEqual(private_fields, expected_private_fields)

    def test_model_doesnotexist_is_raised_when_record_not_found(self):
        with self.assertRaises(CassandraFamilyMember.DoesNotExist):
            not_found_uuid = uuid.uuid4()
            CassandraFamilyMember.objects.allow_filtering().get(id=not_found_uuid)


class TestDjangoCassandraField(CassandraTestCase):
    def setUp(self):
        self.some_uuid = uuid.uuid4()
        self.family_member = CassandraFamilyMember.objects.create(
            id=self.some_uuid,
            first_name="Homer",
            last_name="Simpson",
            is_real=False,
            favourite_number=666,
            favourite_float_number=43.4,
            created_on=datetime.now(),
        )

    def test_attributes(self):
        model_fields = self.family_member._meta._get_fields()

        for field in model_fields:
            allow_null = (
                not field.required
                and not field.is_primary_key
                and not field.partition_key
            ) or field.has_default

            self.assertEqual(field.unique_for_date, None)
            self.assertEqual(field.unique_for_month, None)
            self.assertEqual(field.unique_for_year, None)
            self.assertEqual(field.db_column, None)
            self.assertEqual(field.db_index, field.index)
            self.assertEqual(field.null, allow_null)
            self.assertEqual(field.blank, allow_null)
            self.assertEqual(field.choices, [])
            self.assertEqual(field.flatchoices, [])
            self.assertEqual(field.help_text, "")
            self.assertEqual(field.concrete, True)
            self.assertEqual(field.editable, True)
            self.assertEqual(field.many_to_many, False)
            self.assertEqual(field.many_to_one, False)
            self.assertEqual(field.one_to_many, False)
            self.assertEqual(field.one_to_one, False)
            self.assertEqual(field.hidden, False)
            self.assertEqual(field.serialize, True)
            self.assertEqual(field.name, field.db_field_name)
            self.assertEqual(field.verbose_name, field.db_field_name)
            self.assertEqual(field._verbose_name, field.db_field_name)
            self.assertEqual(field.field, field)
            self.assertEqual(field.model, type(self.family_member))
            self.assertEqual(field.related_query_name(), None)
            self.assertEqual(field.auto_created, False)
            self.assertEqual(field.is_relation, False)
            self.assertEqual(field.remote_field, None)
            self.assertEqual(field.rel, None)
            self.assertEqual(field.rel, None)
            self.assertEqual(field.unique, field.is_primary_key)
            self.assertEqual(field.attname, field.column_name)
            self.assertEqual(field.validators, [])
            self.assertEqual(field.empty_values, list(validators.EMPTY_VALUES))

    def test_methods(self):
        model_fields = self.family_member._meta._get_fields()

        for field in model_fields:
            self.assertEqual(field.get_attname(), field.attname)
            self.assertEqual(field.get_cache_name(), "_{}_cache".format(field.name))

            self.assertEqual(
                field.value_to_string(self.family_member),
                str(getattr(self.family_member, field.name)),
            )

            self.assertEqual(
                field.pre_save(self.family_member, True),
                getattr(self.family_member, field.name),
            )

            self.assertEqual(
                field.get_prep_value(self.family_member.id), self.some_uuid
            )
            self.assertEqual(
                field.get_db_prep_save(self.family_member.id, connection=None),
                self.some_uuid,
            )
            self.assertTrue(isinstance(field.formfield(), fields.CharField))
            self.assertEqual(field.get_internal_type(), field.__class__.__name__)

            self.assertEqual(
                field.get_attname_column(),
                (field.db_field_name, field.db_field_name),
            )
            self.assertEqual(field.get_db_converters(), [])

        field_with_default = self.family_member._meta.get_field("id")
        self.assertTrue(
            isinstance(field_with_default.get_default(), type(self.family_member.id))
        )
        # in Django, 'has_default' is a function, while in python-driver
        # it is a property unfortunately.
        self.assertEqual(field_with_default.has_default, True)

        text_field = self.family_member._meta.get_field("last_name")
        text_field.save_form_data(instance=self.family_member, data="new data")
        self.assertEqual(self.family_member.last_name, "new data")
        self.assertIsNone(field.run_validators(text_field.value))

    def test_methods_which_are_not_implemented_raise(self):
        model_fields = self.family_member._meta._get_fields()

        methods_that_should_raise = (
            "get_choices",
            "get_choices_default",
            "select_format",
            "deconstruct",
            "db_type_suffix",
            "get_prep_lookup",
            "get_db_prep_lookup",
            "set_attributes_from_name",
            "db_parameters",
            "get_col",
        )

        for field in model_fields:
            for method_name in methods_that_should_raise:
                with self.assertRaises(NotImplementedError):
                    getattr(field, method_name)()

    def test_get_pk_value_on_save_returns_true_if_field_has_default(self):
        field_with_default = self.family_member._meta.get_field("id")
        self.assertTrue(
            field_with_default.get_pk_value_on_save(instance=self.family_member),
            self.family_member.id,
        )

    def test_get_pk_value_on_save_returns_none_if_field_no_default(self):
        field_without_default = self.family_member._meta.get_field("last_name")
        self.assertIsNone(
            field_without_default.get_pk_value_on_save(instance=self.family_member),
        )

    def test_formfield_uses_specified_form_class(self):
        text_field = self.family_member._meta.get_field("last_name")
        form_field = text_field.formfield(form_class=fields.BooleanField)
        self.assertTrue(isinstance(form_field, fields.BooleanField))

    def test_field_check_returns_error_when_name_is_pk(self):
        text_field = copy.deepcopy(self.family_member._meta.get_field("last_name"))
        text_field.name = "pk"
        check_errors = text_field.check()
        self.assertEqual(len(check_errors), 1)

    def test_field_check_returns_error_when_name_ends_underscore(self):
        text_field = copy.deepcopy(self.family_member._meta.get_field("last_name"))
        text_field.name = "name_"
        check_errors = text_field.check()
        self.assertEqual(len(check_errors), 1)

    def test_field_check_returns_error_when_name_contains_double_under(self):
        text_field = copy.deepcopy(self.family_member._meta.get_field("last_name"))
        text_field.name = "some__name"
        check_errors = text_field.check()
        self.assertEqual(len(check_errors), 1)

    def test_field_clean(self):
        text_field = copy.deepcopy(self.family_member._meta.get_field("last_name"))
        self.assertEqual(text_field.clean("some val", self.family_member), "some val")

    def test_field_client_raises_when_value_is_not_valid(self):
        text_field = copy.deepcopy(self.family_member._meta.get_field("last_name"))
        with self.assertRaises(CQLValidationError):
            text_field.clean(123, self.family_member)

    def test_get_filter_kwargs_for_object(self):
        text_field = self.family_member._meta.get_field("last_name")
        self.assertEqual(
            text_field.get_filter_kwargs_for_object(obj=self.family_member),
            {"last_name": self.family_member.last_name},
        )

        id_field = self.family_member._meta.get_field("id")
        self.assertEqual(
            id_field.get_filter_kwargs_for_object(obj=self.family_member),
            {"id": self.family_member.id},
        )
