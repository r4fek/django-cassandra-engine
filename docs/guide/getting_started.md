# Django Cassandra Engine - Getting Started

+ Add django-cassandra-engine to `INSTALLED_APPS` in your settings.py file:

```python
    INSTALLED_APPS = ['django_cassandra_engine'] + INSTALLED_APPS
```

!!! note "Important note"
    This app should be **the first app** on **INSTALLED_APPS** list.
    This rule applies only to Django >= 1.7.

+ Change `DATABASES` setting:

``` python
    DATABASES = {
        'default': {
            'ENGINE': 'django_cassandra_engine',
            'NAME': 'db',
            'TEST_NAME': 'test_db',
            'HOST': 'db1.example.com,db2.example.com',
            'OPTIONS': {
                'replication': {
                    'strategy_class': 'SimpleStrategy',
                    'replication_factor': 1
                }
            }
        }
    }
```

+ Define some model(s) in your Django app:

``` python
    #  myapp/models.py
    import uuid
    from cassandra.cqlengine import columns
    from django_cassandra_engine.models import DjangoCassandraModel

    class ExampleModel(DjangoCassandraModel):
        example_id   = columns.UUID(primary_key=True, default=uuid.uuid4)
        example_type = columns.Integer(index=True)
        created_at   = columns.DateTime()
        description  = columns.Text(required=False)
```

+ Run `./manage.py sync_cassandra` in order to sync your models with Cassandra.

+ Done!

## Using with ScyllaDB

Django Cassandra Engine has **full support for ScyllaDB**. The package uses `scylla-driver` for optimal performance with ScyllaDB.

To use Django Cassandra Engine with ScyllaDB, simply point your database configuration to your ScyllaDB cluster:

``` python
    DATABASES = {
        'default': {
            'ENGINE': 'django_cassandra_engine',
            'NAME': 'db',
            'TEST_NAME': 'test_db',
            'HOST': 'scylla-node1.example.com,scylla-node2.example.com',
            'OPTIONS': {
                'replication': {
                    'strategy_class': 'SimpleStrategy',
                    'replication_factor': 3
                }
            }
        }
    }
```

All features work seamlessly with ScyllaDB, including:

* Model synchronization with `sync_cassandra`
* Database migrations
* Test database creation and destruction
* Django admin integration
* Session storage

---

That was simple, right? [I want more!](advanced_usage.md).
