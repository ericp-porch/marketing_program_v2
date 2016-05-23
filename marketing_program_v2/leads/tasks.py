from __future__ import absolute_import

import json

from celery import shared_task

from .models import Leads
from .services import LeadClient


@shared_task
def get_leads(client_id, client_secret, instance):
    l = LeadClient(client_id, client_secret, instance)
    for x in range(35000, 40000, 100):
        range1 = range(x, x + 101)
        build = l.with_path('/rest/v1/leads.json').get_leads('Id', range1).build()
        Leads.object.create_leads(json.loads(build).get('result'))
