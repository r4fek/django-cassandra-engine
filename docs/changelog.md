# CHANGELOG

## Version 0.3.3 (25.05.2015)

* RemovedInDjango19Warnings when using Django >= 1.7 (by @paksu)
* set session.default_consistency_level

## Version 0.3.2 (04.05.2015)

* upgrade cassandra-driver to 2.5.1

## Version 0.3.1 (10.04.2015)

* fix #30: Add support for Django>=1.8
* remove djangotoolbox dependency
* fix #21: Python 3 compatibility

## Version 0.3.0 (03.04.2015)

* fix #29: Update to use integrated cqlengine via cassandra-driver>=2.5.0
  (by @mbeacom and @r4fek)

## Version 0.2.3 (25.03.2015)

* fix #15: test database not used by code under test (by @lsmithso)
* fix #25: working fixtures in `django_cassandra_engine.test.TestCase` 
  (by @slurms)

## Version 0.2.2 (19.01.2015)

* add support for Django==1.5
* add support for Django>=1.7.2
* add `get_engine_from_db_alias` util function

## Version 0.2.1 (16.01.2015)

* update cqlengine to 0.21.0
* move syncing code to `sync_cassandra` command
* Refactor test runner
* separate settings modules to make testing easier
* new test application: `multiapp`
* new `get_cassandra_connections` function to return list of all
  cassandra conncetions defined in DATABASES setting
* `get_cassandra_connection` now accepts alias and name parameters
* `get_cql_models` now returns models for given keyspace

## Version 0.1.8 (13.12.2014)

* add working `Cursor` implementation
* ability to perform raw CQL queries
* improve support for Django 1.7
* present `get_cassandra_connection` helper
* add more tests

## Version 0.1.7 (24.11.2014)

* revert broken consistency fix (thanks to @danandersonasc)

## Version 0.1.6 (24.11.2014)

* fix passing proper consistency option to `cqlengine.setup`
* add more tests
* bump cqlengine to 0.20.0

## Version 0.1.5 (17.11.2014)

* ability to set `cassandra.cluster.Session` options like `default_timeout`
(thanks @danpilch)

## Version 0.1.4 (01.11.2014)

* add support for authorization (thanks to @drivard)

## Version 0.1.3 (20.10.2014)

* more tests for Connection class
* presesnt `sync_cassandra` management command

## Version 0.1.2 (20.10.2014)

* add support for uWSGI

## Version 0.1.1 (17.10.2014)

* fix exceptions in Django 1.7
* override migrate and runserver commands

## Version 0.1.0 (08.10.2014)

* Change status to **Production/Stable**
* Bump cqlengine to v.0.19
* Update docs

## Version 0.0.7 (02.10.2014)

* Support for more connection options (thanks to @mwiewiorski)

## Version 0.0.6 (03.09.2014)

* Add support for Django 1.7

## Version 0.0.5 (29.08.2014)

* Improved models discovery
* Call the standard syncdb if the engine is not django_cassandra_engine
  (thanks to @ratm)
* Travis integration

## Version 0.0.4 (22.08.2014)

* Feature: add support for *flush* management command
* Bugfix: lock dependencies in setup.py
* add more tests


## Version 0.0.3 (21.08.2014)

* Bugfix: Fix some issue in *flush* command (add dummy support for Django 1.6.6)


## Version 0.0.2 (04.08.2014)

* Bugfix: Do not reconnect on every request


## Version 0.0.1 (31.07.2014)

* Feature: allow to define cassandra backend in settings.py
* Feature: connect to the Cassandra database automatically on app startup
* Feature: *syncdb* management command
* Feature: support for django test framework
* Feature: Support for Cqlengine Object Mapper
