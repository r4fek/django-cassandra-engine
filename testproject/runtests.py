#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
from subprocess import check_call as execute
from types import ModuleType


def run_tests(foo, settings='settings', extra=(), test_builtin=False):
    if isinstance(foo, ModuleType):
        settings = foo.__name__
        apps = list(foo.INSTALLED_APPS)
    else:
        apps = list(foo)

    if not test_builtin:
        apps = filter(lambda name: not name.startswith('django.contrib.'),
                      apps)

    # pre-1.6 test runners don't understand full module names
    if django.VERSION < (1, 6):
        apps = [app.replace('django.contrib.', '') for app in apps]
        apps = filter(lambda name: not name.startswith('testproject.'),
                      apps)

    print '\n============================\n' \
          'Running tests with settings: {}\n' \
          '============================\n'.format(settings)
    return execute(
        ['./manage.py', 'test', '--settings', settings] + list(extra) + apps)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "testproject.settings.default_only_cassandra")
    import django
    if django.VERSION[0:2] >= (1, 7):
        django.setup()

    import testproject.settings.default_only_cassandra as default_only_cass
    import testproject.settings.secondary_cassandra as secondary_cassandra
    import testproject.settings.multi_cassandra as multi_cassandra

    run_tests(default_only_cass)
    run_tests(secondary_cassandra)
    run_tests(multi_cassandra)
