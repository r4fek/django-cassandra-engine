#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
from subprocess import check_call as execute
from types import ModuleType

import django
from django.utils.importlib import import_module


os.environ["DJANGO_SETTINGS_MODULE"] = "settings.default_only_cassandra"

test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)


def run_tests(foo, settings='settings', extra=(), test_builtin=False):
    if isinstance(foo, ModuleType):
        settings = foo.__name__
        apps = list(foo.INSTALLED_APPS)
    else:
        apps = list(foo)

    if not test_builtin:
        apps = [
            name for name in apps if not name.startswith('django.contrib.')]

    # pre-1.6 test runners don't understand full module names
    if django.VERSION < (1, 6):
        apps = [app.replace('django.contrib.', '') for app in apps]
        apps = [name for name in apps if not name.startswith('testproject.')]

    os.chdir(test_dir)
    print('\n============================\n'
          'Running tests with settings: {}\n'
          '============================\n'.format(settings))
    return execute(
        ['./manage.py', 'test', '--settings', settings] + list(extra) + apps)


def main():

    default_only_cass = import_module(
        'settings.default_only_cassandra')
    secondary_cassandra = import_module(
        'settings.secondary_cassandra')
    multi_cassandra = import_module(
        'settings.multi_cassandra')

    if django.VERSION[0:2] >= (1, 7):
        django.setup()

    run_tests(default_only_cass)
    run_tests(secondary_cassandra)
    run_tests(multi_cassandra)
    sys.exit(0)

if __name__ == "__main__":
    main()
