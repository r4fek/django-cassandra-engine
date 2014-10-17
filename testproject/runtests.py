#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os
import django


def run_tests():

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testproject.settings")
    
    if django.VERSION >= (1, 7):
        django.setup()

    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner(
        verbosity=1, interactive=False, failfast=False)

    return test_runner.run_tests(['testproject.app'])


if __name__ == "__main__":
    failures = run_tests()
    sys.exit(failures)
