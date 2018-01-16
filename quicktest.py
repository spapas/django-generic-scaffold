# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import argparse
from django.conf import settings
import django


class QuickDjangoTest(object):
    """
    A quick way to run the Django test suite without a fully-configured project.

    Example usage:

        >>> QuickDjangoTest(apps=['app1', 'app2'], db='sqlite')

    Based on a script published by Lukasz Dziedzia at:
    http://stackoverflow.com/questions/3841725/how-to-launch-tests-for-django-reusable-app
    """
    DIRNAME = os.path.dirname(__file__)
    INSTALLED_APPS = [
        'django.contrib.staticfiles',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
    ]

    def __init__(self, *args, **kwargs):
        self.apps = kwargs.get('apps', [])
        self.database= kwargs.get('db', 'sqlite')
        self.run_tests()

    def run_tests(self):


        django_settings = {
            'DATABASES':{
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                }
            },
            'INSTALLED_APPS':self.INSTALLED_APPS + self.apps,
            'STATIC_URL':'/static/',
            'ROOT_URLCONF':'generic_scaffold.tests',
            'SILENCED_SYSTEM_CHECKS':['1_7.W001']
        }

        if django.VERSION >= (1, 8, 0):
            django_settings['TEMPLATES'] = [{
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.template.context_processors.debug',
                            'django.template.context_processors.request',
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',
                        ],
                    },
                }]

        settings.configure(**django_settings)

        if django.VERSION >= (1, 7, 0):
            # see: https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
            django.setup()

        from django.test.runner import DiscoverRunner as Runner

        failures = Runner().run_tests(self.apps, verbosity=1)
        if failures:  # pragma: no cover
            sys.exit(failures)

if __name__ == '__main__':
    QuickDjangoTest(apps=['generic_scaffold'], db='sqlite3')
