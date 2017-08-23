# -*- coding: utf-8 -*-
"""
    setup.py
    ~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from setuptools import setup, find_packages

from vishnu import __version__

setup(
    name="vishnu",
    version=__version__,
    description='Sessions for the Google App Engine Python runtime',
    url='https://github.com/anomaly/vishnu.git',
    long_description=open("README.rst").read(),
    download_url='https://github.com/anomaly/vishnu/archive/' + __version__ + '.tar.gz',
    license='Apache 2.0',
    author='Anomaly Software',
    author_email='support@anomaly.net.au',
    maintainer='Anomaly Software',
    maintainer_email='support@anomaly.net.au',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "future",
        "pycrypto==2.6.1"
    ],
    tests_require=[
        'pytest',
        'redis',
        'pylibmc',
        'pymemcache',
        'python-memcached',
        'falcon',
        'webtest'
    ],
    setup_requires=['pytest-runner'],
    extras_require={
        'devel': ['tox', 'tox-pyenv', 'pytest'],
        'pylibmc': ['pylibmc'],
        'pymemcache': ['pymemcache'],
        'python-memcached': ['python-memcached'],
        'redis': ['redis'],
    }
)
