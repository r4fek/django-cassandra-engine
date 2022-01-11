#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from importlib import import_module
from subprocess import check_call as execute
from types import ModuleType
import os
import sys

import django

os.environ["DJANGO_SETTINGS_MODULE"] = "settings.default_only_cassandra"

test_dir = os.path.dirname(__file__)
test_dir_abspath = os.path.split(os.path.abspath(__file__))[0]

sys.path.insert(0, test_dir)


def run_tests(foo, settings="settings", extra=(), test_builtin=False):
    if isinstance(foo, ModuleType):
        settings = foo.__name__
        apps = list(foo.INSTALLED_APPS)
    else:
        apps = list(foo)

    if not test_builtin:
        apps = [name for name in apps if not name.startswith("django.contrib.")]

    os.chdir(test_dir_abspath)
    print(
        "\n============================\n"
        "Running tests with settings: {}\n"
        "============================\n".format(settings)
    )
    return execute(
        ["./manage.py", "test", "-v", "2", "--settings", settings] + list(extra) + apps
    )


def main():

    default_cass = import_module("settings.default_cassandra")
    default_only_cass = import_module("settings.default_only_cassandra")
    secondary_cassandra = import_module("settings.secondary_cassandra")
    multi_cassandra = import_module("settings.multi_cassandra")
    metadata_disabled = import_module("settings.metadata_disabled")

    django.setup()

    run_tests(default_cass)
    run_tests(default_only_cass)
    run_tests(secondary_cassandra)
    run_tests(multi_cassandra)
    run_tests(metadata_disabled)
    sys.exit(0)


if __name__ == "__main__":
    main()
