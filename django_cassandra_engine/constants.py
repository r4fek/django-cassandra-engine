
ORDER_BY_WARN = (
    '.order_by() with column "{col}" failed! '
    'Falling back to ordering in python. \n'
    'Exception was: {exc}'
)
ORDER_BY_ERROR_HELP = (
    'To enable fallback order_by() python implementation,\n'
    'set "CASSANDRA_FALLBACK_ORDER_BY_PYTHON = True" in Django Settings.'
)
PK_META_MISSING_HELP = (
    '\nOn Django Cassandra Models with more than one primary_key field,\n'
    'The model {} must specify class Meta attribute \'get_pk_field\'.\n'
    'E.g.\n'
    'class Meta:\n'
    '  get_pk_field=\'id\'\n'
    'So that Django knows which primary key field to use in queryies '
    'such as Model.objects.get(pk=123)'
)
