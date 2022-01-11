"""Handle package compatibility."""

try:
    from dse import cqlengine
    from dse.auth import PlainTextAuthProvider
    from dse.cluster import Cluster, Session
    from dse.cqlengine import CQLEngineException, columns, connection, management, query
    from dse.cqlengine.management import create_keyspace_simple, drop_keyspace
    from dse.cqlengine.models import (
        BaseModel,
        ColumnDescriptor,
        Model,
        ModelDefinitionException,
        ModelException,
        ModelMetaClass,
    )
    from dse.util import OrderedDict
except ImportError:
    try:
        from cassandra import cqlengine
        from cassandra.auth import PlainTextAuthProvider
        from cassandra.cluster import Cluster, Session
        from cassandra.cqlengine import (
            CQLEngineException,
            columns,
            connection,
            management,
            query,
        )
        from cassandra.cqlengine.management import create_keyspace_simple, drop_keyspace
        from cassandra.cqlengine.models import (
            BaseModel,
            ColumnDescriptor,
            Model,
            ModelDefinitionException,
            ModelException,
            ModelMetaClass,
        )
        from cassandra.util import OrderedDict
    except ImportError:
        raise ImportError(
            "You must install either dse-driver or " + "cassandra-driver!"
        )
