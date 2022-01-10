import uuid

import django

from common.forms import CassandraFamilyMemberForm
from common.models import CassandraFamilyMember
from django_cassandra_engine.test import TestCase as CassandraTestCase


class TestModelForm(CassandraTestCase):
    def setUp(self):
        self.some_uuid = uuid.uuid4()
        self.family_member = CassandraFamilyMember.objects.create(
            id=self.some_uuid,
            first_name="Homer",
            last_name="Simpson",
            is_real=False,
            favourite_number=666,
            favourite_float_number=43.4,
        )

    def test_form_save(self):
        form = CassandraFamilyMemberForm(
            data=dict(
                id=self.some_uuid,
                first_name="Homer",
                last_name="Simpson",
                is_real=False,
                favourite_number=666,
                favourite_float_number=43.4,
            )
        )
        instance = form.save()

        self.assertEqual(instance.id, str(self.some_uuid))

    def test_form_edit(self):
        existing = self.family_member

        # when updating a django cassandra model,
        # he primary and partition key values need to be specific
        form = CassandraFamilyMemberForm(
            data=dict(
                id=existing.id,
                favourite_float_number=existing.favourite_float_number,
                first_name="Marge",
                last_name=existing.last_name,
            ),
            instance=existing,
        )
        form.is_valid()
        self.assertEqual(form.errors, {})
        self.assertTrue(form.is_valid())

        updated = form.save()

        self.assertEqual(updated.first_name, "Marge")
