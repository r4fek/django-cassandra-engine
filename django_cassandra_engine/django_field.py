from __future__ import unicode_literals

from django.utils.encoding import smart_text


def value_from_object(self, obj):
    """
    Returns the value of this field in the given model instance.
    """
    return getattr(obj, self.attname)


def value_to_string(self, obj):
    """
    Returns a string value of this field from the passed obj.
    This is used by the serialization framework.
    """
    return smart_text(self.value_from_object(obj))
