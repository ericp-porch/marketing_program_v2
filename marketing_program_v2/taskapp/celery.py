from __future__ import absolute_import

import os
from sys import path

from celery import Celery

# set the default Django settings module for the 'celery' program.
from django.apps import AppConfig
from django.conf import settings  # noqa
from os.path import dirname, abspath

SITE_ROOT = dirname(dirname(dirname(abspath(__file__))))
path.append(SITE_ROOT)

if not settings.configured:
    print SITE_ROOT
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover

app = Celery('taskapp')


class CeleryConfig(AppConfig):
    name = 'marketing_program_v2.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings')
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
