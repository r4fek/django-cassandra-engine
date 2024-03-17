# Django Cassandra Engine - CHANGELOG


## Version 1.9.0 (17.03.2024)

* Support Django up to 4.2
* Add support for Python 3.12

## Version 1.8.0 (02.02.2023)

* Drop support for Django 3.1
* Support Django up to 4.1
* Add support for Python 3.11

## Version 1.7.0 (11.01.2022)

* Fix(command/dbshell): Avoid raise TypeError when django-3.2 pass `options['parameters']` (#154) - thanks @icycandle!
* Support Django 4.x
* Drop support for Python <3.7
* replace `cassandra-driver` with `scylla-driver` to better support ScyllaDB (Scylla driver is fully compatible with Cassandra)
* Get rid of travis build system in favor of Github Actions (faster build times, better integration with Github)
* Reformat entire codebase with flake8, isort and black
* Add code style check to the build process
* Use Poetry to install the package and maintain dependencies

## Version 1.6.3 (26.07.2021)

* Support cloud cred bundle (#142)

## Version 1.6.2 (19.05.2021)

* Add support for Django 3.1 and 3.2
* Fix #140: TypeError: sql_flush() got an unexpected keyword argument

## Version 1.6.1 (20.03.2020)

* Updated requirements #136 (by @hsamfm)

## Version 1.6.0 (09.03.2020)

* Support Django 3.x #135
* Fix tests
* Update cassandra-driver to 3.22.0

## Version 1.5.5 (30.01.2019)

* Create the test keyspace not in the runtime keyspace (by @andydawkins)

## Version 1.5.4 (01.10.2018)

* Upgrade `Django` and `cassandra-driver` deps

## Version 1.5.3 (26.07.2018)

* Turn `schema_metadata_enabled` on while syncing database
* Make get_cql_models connection aware

## Version 1.5.0 (14.06.2018)

* Support multiple cassandra databases
* Add docker-compose setup for better testing

## Version 1.4.0 (15.02.2018)

* Support Django 2.0.x
* Update cassandra-driver to 3.13.0

## Version 1.3.0 (16.11.2017)

* Allow "schema_metadata_enabled" set to False in the connection options #105
  (by awesome @bowensong)
* Update cassandra-driver to 3.12.0

## Version 1.2.2 (29.08.2017)

* Fix CassandraDatabaseSchemaEditor.create_model (#100)

## Version 1.2.1 (11.08.2017)

* Add dse-driver support #98 (by @mbeacom)

## Version 1.2.0 (01.08.2017)

* Update cassandra-driver to 3.11.0
* Fix #93: Each query seems to execute a count()
* Fix #91: Set CQLENG_ALLOW_SCHEMA_MANAGEMENT variable if was not present

## Version 1.1.1 (26.04.2017)

* Fix #90: Breaks BooleanField with provided default value: can't save False
  via admin UI project-wide if using django-cassandra-engine in same project

## Version 1.1.0 (09.04.2017)

* Fix #89: Support Django 1.11 + update `cassandra-driver` to 3.8.1

## Version 1.0.2 (04.11.2016)

* Connect to Cassandra before importing models

## Version 1.0.1 (31.10.2016)

* Fix #82: Support `cassandra-driver==3.7.1`

## Version 1.0 (25.10.2016)

* Fix #66: `_meta` API support (by awesome @richardasaurus)

## Version 0.11.1 (01.09.2016)

* Fix for #70 "AttributeError: operators (by @bezineb5)
* Fix #72: Django 1.10 `makemigrations` issue
* Fix #74: supress emit_post_migrate_signal in sync_cassandra (by @jamey)

## Version 0.11.0 (05.08.2016)

* Fix #69: Replace NoArgsCommand with BaseCommand to accommodate 1.10 upgrade (by @BenBrostoff)
* Update `cassandra-driver` to 3.6.0

## Version 0.10.1 (22.07.2016)

* Update `cassandra-driver` to 3.5.0

## Version 0.10.0 (10.06.2016)

* Update to emit post migrate signal (by @kamal-una)
* Update `cassandra-driver` to 3.4.1

## Version 0.9.0 (11.05.2016)

* Update `cassandra-driver` to 3.3.0
* Update FAQ about uwsgi support

## Version 0.8.1 (20.04.2016)

* Update `cassandra-driver` to 3.2.2 (check PYTHON-547).

## Version 0.8.0 (18.04.2016)

* Update `cassandra-driver` to 3.2.1

## Version 0.7.4 (23.03.2016)

* Fix error thrown in `runserver` command

## Version 0.7.3 (21.03.2016)

* Minor fix in sessions backend (remove pk from `Session.expire_date`)

## Version 0.7.2 (15.03.2016)

* Locked `cassandra-driver` version in `setup.py` (fixup)

## Version 0.7.1 (15.03.2016)

* Update `cassandra-driver` to 3.1.1 due to `PYTHON-522`
* Fix #55: pypi page looks strange

## Version 0.7.0 (11.03.2016)

* Update `cassandra-driver` to 3.1.0
* Fix `syncdb` command in `Django>=1.9`
* Fix not working `django.contrib.admin` app when `dce` is used
* Add `tox` for running tests easily
* Introduce `sessions` app
* Update docs

## Version 0.6.6 (04.03.2016)

* Update requirements.txt to support `Django<1.10`

## Version 0.6.5 (22.02.2016)

* Fix support for latest `django-nose==1.4.3`

## Version 0.6.4 (05.02.2016)

* Get rid of race condition in `CassandraConnection.setup`
* Remove not needed reconnecting on `@postfork`

## Version 0.6.3 (08.01.2016)

* Major improvement in tests execution time

## Version 0.6.2 (08.12.2015)

* Support Django==1.9

## Version 0.6.1 (07.12.2015)

* Fix `CassandraConnection.setup` method (thanks @mateuszm!)

## Version 0.6.0 (25.11.2015)

* Update cassandra-driver to 0.3.0

## Version 0.5.2 (04.10.2015)

* Update cassandra-driver to 2.7.2

## Version 0.5.1 (14.09.2015)

* fix #44: Fix migrate command when working in a multi db environment (by @paksu)

## Version 0.5.0 (26.08.2015)

* Fix `CassandraDatabaseFeatures.supports_transactions` (thanks @slurms)
* Update cassandra-driver to 2.7.1

## Version 0.4.0 (21.07.2015)

* Update cassandra-driver to 2.6.0

## Version 0.3.4 (01.07.2015)

* Set Session attributes in class instead of local instance (by @mateuszm)

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
