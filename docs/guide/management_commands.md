# Django Cassandra Engine - Management Commands

These Django management commands will make your life a lot easier.

## `sync_cassandra`

Synchronizes your models with Cassandra.

``` sh
    $ python manage.py sync_cassandra
    
    Syncing app.models.ExampleModel
    Syncing app.models.ExampleModel2
    Syncing app.models.TestProjectModel

```

## `migrate`

Synchronizes your models with Cassandra.

``` sh
    $ python manage.py migrate --database default
    
    Syncing app.models.ExampleModel
    Syncing app.models.ExampleModel2
    Syncing app.models.TestProjectModel

```

## `flush`

Flushes your database.

``` sh
    $ python manage.py flush
```

## `dbshell`

Quick access to dbshell via `cqlsh`.

If you need to perform raw `CQL` query on your keyspace just run:

``` sh
    $ python manage.py dbshell
    
    Connected to Test Cluster at 127.0.0.1:9042.
    [cqlsh 5.0.1 | Cassandra 2.1.4 | CQL spec 3.2.0 | Native protocol v3]
    Use HELP for help.
    cqlsh:your_keyspace>
```

## `inspectdb`

Introspects Cassandra database. It shows only model names and db tables.

``` python
    $ python manage.py inspectdb
    
    class Session(models.Model):

        class Meta:
            managed = False
            db_table = 'session'
    
    
    class ExampleModel2(models.Model):
    
        class Meta:
            managed = False
            db_table = 'example_model2'
    
    
    class ExampleModel(models.Model):
    
        class Meta:
            managed = False
            db_table = 'example_model'
    
    
    class TestProjectModel(models.Model):
    
        class Meta:
            managed = False
            db_table = 'test_project_model'
```

---

Almost done! Show me how to [test](tests.md) my app.
