from __future__ import absolute_import

from sys import path

import os
from celery import Celery
from os.path import dirname, abspath

SITE_ROOT = dirname(dirname(dirname(abspath(__file__))))

path.append(SITE_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('leads',
             broker='amqp://guest@localhost//',
             backend='amqp://',
             include=['leads.tasks'])

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
