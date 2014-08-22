from setuptools import setup, find_packages

import django_cassandra_engine as meta

DESCRIPTION = 'Django Cassandra Engine - the Cassandra backend for Django'
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
    keywords='django cassandra engine backend driver database nonrel cqlengine',
    download_url='http://github.com/r4fek/django-cassandra-engine/tarball/master',
    license='2-clause BSD',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=['djangotoolbox==1.6.2', 'cqlengine==0.18.1'],
    packages=find_packages(
        exclude=['tests', 'tests.*', 'testproject', 'testproject.*']),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        "Environment :: Plugins",
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
