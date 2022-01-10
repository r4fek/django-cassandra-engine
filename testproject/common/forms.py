from django.forms import ModelForm

from common.models import CassandraFamilyMember


class CassandraFamilyMemberForm(ModelForm):
    class Meta:
        model = CassandraFamilyMember
        exclude = ("created_on",)
