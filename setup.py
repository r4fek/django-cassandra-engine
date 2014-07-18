from setuptools import setup, find_packages

import django_cassandra_engine as meta

DESCRIPTION = 'Cassandra backend for Django-nonrel'
LONG_DESCRIPTION = None

try:
    LONG_DESCRIPTION = open('README.rst').read()
except IOError:
    pass

setup(
    name='django-cassandra-engine',
    version='.'.join(map(str, meta.__version__)),
    author=meta.__author__,
    author_email=meta.__contact__,
    url=meta.__homepage__,
    license='2-clause BSD',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=['cassandra-driver', 'djangotoolbox>=1.6.0', 'cqlengine'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
