#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os


def run_tests():

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testproject.settings")
    
    try:
        # Django 1.7 specific
        import django
        django.setup()
    except:
        pass
    
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner(
        verbosity=1, interactive=False, failfast=False)

    failures = test_runner.run_tests(['testproject.app'])

    return failures


if __name__ == "__main__":
    failures = run_tests()
    sys.exit(failures)
