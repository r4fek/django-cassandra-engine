from __future__ import absolute_import, unicode_literals

import inspect
from django.apps import AppConfig as DjangoAppConfig
import django.forms.models


def construct_instance(form, instance, fields=None, exclude=None):
    """
    Taken from django.forms.models.construct_instance
    altered to support cqlengine models (see field_has_default logic)
    """
    from django.db import models
    opts = instance._meta

    cleaned_data = form.cleaned_data
    file_field_list = []
    for f in opts.fields:
        if not f.editable or isinstance(f, models.AutoField) \
                or f.name not in cleaned_data:
            continue
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        # Leave defaults for fields that aren't in POST data, except for
        # checkbox inputs because they don't appear in POST data if not checked

        # cqlengine support logic start
        if inspect.ismethod(f.has_default):
            # django model
            field_has_default = f.has_default()
        else:
            # cqlengine model
            field_has_default = f.has_default
        # cqlengine support logic end

        if (field_has_default and form.add_prefix(f.name) not in form.data and
                not getattr(form[f.name].field.widget,
                            'dont_use_model_field_default_for_empty_data',
                            False)):
            continue
        # Defer saving file-type fields until after the other fields, so a
        # callable upload_to can use the values from other fields.
        if isinstance(f, models.FileField):
            file_field_list.append(f)
        else:
            f.save_form_data(instance, cleaned_data[f.name])

    for f in file_field_list:
        f.save_form_data(instance, cleaned_data[f.name])

    return instance

# patching so that Django ModelForms can work with cqlengine models
django.forms.models.construct_instance = construct_instance


class AppConfig(DjangoAppConfig):
    name = 'django_cassandra_engine'

    def ready(self):
        from django_cassandra_engine.utils import get_cassandra_connections
        for _, conn in get_cassandra_connections():
            conn.connect()
