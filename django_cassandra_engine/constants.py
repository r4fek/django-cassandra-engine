
ORDER_BY_WARN = (
    '.order_by() with column "{col}" failed! '
    'Falling back to ordering in python. \n'
    'Exception was: {exc}'
)
ORDER_BY_ERROR_HELP = (
    'To enable fallback order_by() python implementation,\n'
    'set "CASSANDRA_FALLBACK_ORDER_BY_PYTHON = True" in Django Settings.'
)
CASSANDRA_DRIVER_COMPAT_VERSIONS = ('3.3.0', '3.4.0', '3.4.1')
