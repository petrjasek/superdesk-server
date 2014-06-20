#!/usr/bin/env python

from setuptools import setup, find_packages

LONG_DESCRIPTION = open('README.md').read()

setup(
    name='Superdesk-Server',
    version='0.1.2',
    description='Superdesk REST API server',
    long_description=LONG_DESCRIPTION,
    author='petr jasek',
    author_email='petr.jasek@sourcefabric.org',
    url='https://github.com/superdesk/superdesk-server',
    license='GPLv3',
    platforms=['any'],
    packages=find_packages(),
    install_requires=[
        'blinker==1.3',
        'celery[redis]==3.1.11',
        'eve==0.4',
        'eve-docs==0.1.2',
        'eve-elastic==0.1.10',
        'flask==0.10.1',
        'flask-script==2.0.3',
        'pillow==2.4.0',
        'python-magic==0.4.6',
        'simplejson==3.5.2',
    ],

    scripts=['settings.py', 'app.py', 'wsgi.py', 'manage.py', 'docs.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
