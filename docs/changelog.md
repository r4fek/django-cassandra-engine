# CHANGELOG

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
