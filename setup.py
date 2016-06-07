# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import django_cassandra_engine as meta


DESCRIPTION = 'Django Cassandra Engine - the Cassandra backend for Django'


try:
    with open('README.rst', 'rb') as f:
        LONG_DESCRIPTION = f.read().decode('utf-8')
except IOError:
    with open('README.md', 'rb') as f:
        LONG_DESCRIPTION = f.read().decode('utf-8')

with open('requirements.txt', 'r') as f:
    DEPENDENCIES = f.read().splitlines()


setup(
    name='django-cassandra-engine',
    version='.'.join(map(str, meta.__version__)),
    author=meta.__author__,
    author_email=meta.__contact__,
    url=meta.__homepage__,
    keywords='django cassandra engine backend driver wrapper database nonrel '
             'cqlengine',
    download_url='https://github.com/r4fek/django-cassandra-engine/tarball/master',
    license='2-clause BSD',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=DEPENDENCIES,
    packages=find_packages(
        exclude=['tests', 'tests.*', 'testproject', 'testproject.*']),
    test_suite='testproject.runtests.main',
    tests_require=['mock==1.0.1', 'django-nose'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        "Environment :: Plugins",
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Database',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
