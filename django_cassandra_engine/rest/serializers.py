import warnings

from django.core.validators import DecimalValidator
from django.utils.text import capfirst
from rest_framework import serializers
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    ModelField,
    models,
    postgres_fields,
)
from rest_framework.utils.field_mapping import (
    ClassLookupDict,
    needs_label,
    NUMERIC_FIELD_TYPES,
    validators,
)

from ..compat import columns


class DjangoCassandraModelSerializer(serializers.ModelSerializer):
    serializer_field_mapping = {
        columns.Text: serializers.CharField,
        columns.UUID: serializers.CharField,
        columns.Integer: serializers.IntegerField,
        columns.TinyInt: serializers.IntegerField,
        columns.SmallInt: serializers.IntegerField,
        columns.BigInt: serializers.IntegerField,
        columns.VarInt: serializers.IntegerField,
        columns.Counter: serializers.IntegerField,
        columns.Date: serializers.DateTimeField,
        columns.Float: serializers.FloatField,
        columns.Double: serializers.FloatField,
        columns.Decimal: serializers.DecimalField,
        columns.Boolean: serializers.BooleanField,
        columns.DateTime: serializers.DateTimeField,
        columns.List: serializers.ListField,
    }

    def get_field_kwargs(self, field_name, model_field):
        """
        Creates a default instance of a basic non-relational field.
        """
        kwargs = {}
        validator_kwarg = list(model_field.validators)

        # The following will only be used by ModelField classes.
        # Gets removed for everything else.
        kwargs['model_field'] = model_field

        if model_field.verbose_name and needs_label(model_field, field_name):
            kwargs['label'] = capfirst(model_field.verbose_name)

        if model_field.help_text:
            kwargs['help_text'] = model_field.help_text

        max_digits = getattr(model_field, 'max_digits', None)
        if max_digits is not None:
            kwargs['max_digits'] = max_digits

        decimal_places = getattr(model_field, 'decimal_places', None)
        if decimal_places is not None:
            kwargs['decimal_places'] = decimal_places

        if isinstance(model_field, models.TextField):
            kwargs['style'] = {'base_template': 'textarea.html'}

        if isinstance(model_field, models.AutoField) \
                or not model_field.editable:
            # If this field is read-only, then return early.
            # Further keyword arguments are not valid.
            kwargs['read_only'] = True
            return kwargs

        if model_field.has_default or model_field.blank or model_field.null:
            kwargs['required'] = False

        if model_field.null and not isinstance(model_field,
                                               models.NullBooleanField):
            kwargs['allow_null'] = True

        if model_field.blank and (
            isinstance(model_field, models.CharField) or
            isinstance(model_field, models.TextField) or
            isinstance(model_field, columns.Text)
        ):
            kwargs['allow_blank'] = True

        if isinstance(model_field, models.FilePathField):
            kwargs['path'] = model_field.path

            if model_field.match is not None:
                kwargs['match'] = model_field.match

            if model_field.recursive is not False:
                kwargs['recursive'] = model_field.recursive

            if model_field.allow_files is not True:
                kwargs['allow_files'] = model_field.allow_files

            if model_field.allow_folders is not False:
                kwargs['allow_folders'] = model_field.allow_folders

        if model_field.choices:
            # If this model field contains choices, then return early.
            # Further keyword arguments are not valid.
            kwargs['choices'] = model_field.choices
            return kwargs

        # Our decimal validation is handled in the field code,
        # not validator code.
        # (In Django 1.9+ this differs from previous style)
        if isinstance(model_field, models.DecimalField) and DecimalValidator:
            validator_kwarg = [
                validator for validator in validator_kwarg
                if not isinstance(validator, DecimalValidator)
            ]

        # Ensure that max_length is passed explicitly as a keyword arg,
        # rather than as a validator.
        max_length = getattr(model_field, 'max_length', None)
        if max_length is not None and (
                    isinstance(model_field, models.CharField) or
                    isinstance(model_field, models.TextField)):
            kwargs['max_length'] = max_length
            validator_kwarg = [
                validator for validator in validator_kwarg
                if not isinstance(validator, validators.MaxLengthValidator)
            ]

        # Ensure that min_length is passed explicitly as a keyword arg,
        # rather than as a validator.
        min_length = next((
            validator.limit_value for validator in validator_kwarg
            if isinstance(validator, validators.MinLengthValidator)
        ), None)
        if min_length is not None and isinstance(model_field,
                                                 models.CharField):
            kwargs['min_length'] = min_length
            validator_kwarg = [
                validator for validator in validator_kwarg
                if not isinstance(validator, validators.MinLengthValidator)
            ]

        # Ensure that max_value is passed explicitly as a keyword arg,
        # rather than as a validator.
        max_value = next((
            validator.limit_value for validator in validator_kwarg
            if isinstance(validator, validators.MaxValueValidator)
        ), None)
        if max_value is not None and isinstance(model_field,
                                                NUMERIC_FIELD_TYPES):
            kwargs['max_value'] = max_value
            validator_kwarg = [
                validator for validator in validator_kwarg
                if not isinstance(validator, validators.MaxValueValidator)
            ]

        # Ensure that max_value is passed explicitly as a keyword arg,
        # rather than as a validator.
        min_value = next((
            validator.limit_value for validator in validator_kwarg
            if isinstance(validator, validators.MinValueValidator)
        ), None)
        if min_value is not None and isinstance(model_field,
                                                NUMERIC_FIELD_TYPES):
            kwargs['min_value'] = min_value
            validator_kwarg = [
                validator for validator in validator_kwarg
                if not isinstance(validator, validators.MinValueValidator)
            ]

        # URLField does not need to include the URLValidator argument,
        # as it is explicitly added in.
        if isinstance(model_field, models.URLField):
            validator_kwarg = [
                validator for validator in validator_kwarg
                if not isinstance(validator, validators.URLValidator)
            ]

        # EmailField does not need to include the validate_email argument,
        # as it is explicitly added in.
        if isinstance(model_field, models.EmailField):
            validator_kwarg = [
                validator for validator in validator_kwarg
                if validator is not validators.validate_email
            ]

        # SlugField do not need to include the 'validate_slug' argument,
        if isinstance(model_field, models.SlugField):
            validator_kwarg = [
                validator for validator in validator_kwarg
                if validator is not validators.validate_slug
            ]

        # IPAddressField do not need to include the 'validate_ipv46_address'
        # argument,
        if isinstance(model_field, models.GenericIPAddressField):
            validator_kwarg = [
                validator for validator in validator_kwarg
                if validator is not validators.validate_ipv46_address
            ]

        if getattr(model_field, 'unique', False):
            warnings.warn(
                'UniqueValidator is currently not supported '
                'in DjangoCassandraSerializer'
            )

        if validator_kwarg:
            kwargs['validators'] = validator_kwarg

        return kwargs

    def build_standard_field(self, field_name, model_field):
        """
        Create regular model fields.
        """
        field_mapping = ClassLookupDict(self.serializer_field_mapping)

        field_class = field_mapping[model_field]
        field_kwargs = self.get_field_kwargs(field_name, model_field)
        if 'choices' in field_kwargs:
            # Fields with choices get coerced into `ChoiceField`
            # instead of using their regular typed field.
            field_class = self.serializer_choice_field
            # Some model fields may introduce kwargs that would not be valid
            # for the choice field. We need to strip these out.
            # Eg. models.DecimalField(max_digits=3, decimal_places=1,
            #                         choices=DECIMAL_CHOICES)

            valid_kwargs = {
                'read_only', 'write_only',
                'required', 'default', 'initial', 'source',
                'label', 'help_text', 'style',
                'error_messages', 'validators', 'allow_null', 'allow_blank',
                'choices'
            }
            for key in list(field_kwargs.keys()):
                if key not in valid_kwargs:
                    field_kwargs.pop(key)

        if not issubclass(field_class, ModelField):
            # `model_field` is only valid for the fallback case of
            # `ModelField`, which is used when no other typed field
            # matched to the model field.
            field_kwargs.pop('model_field', None)

        if not issubclass(field_class, CharField) and not \
                issubclass(field_class, ChoiceField):
            # `allow_blank` is only valid for textual fields.
            field_kwargs.pop('allow_blank', None)

        if postgres_fields and isinstance(model_field,
                                          postgres_fields.ArrayField):
            # Populate the `child` argument on `ListField` instances generated
            # for the PostgrSQL specfic `ArrayField`.
            child_model_field = model_field.base_field
            child_field_class, child_field_kwargs = self.build_standard_field(
                'child', child_model_field
            )
            field_kwargs['child'] = child_field_class(**child_field_kwargs)

        return field_class, field_kwargs
