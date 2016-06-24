from __future__ import absolute_import

import json

from marketing_program_v2.celery import app
from marketing_program_v2.leads.models import Leads
from marketing_program_v2.leads.services import LeadClient


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task
def get_leads(fields, client_id, client_secret, instance):
    l = LeadClient(client_id, client_secret, instance)
    for x in range(0, 1000, 100):
        range_of_ids = range(x, x + 101)
        json_raw = l.with_path('/rest/v1/leads.json').get_leads('Id', range_of_ids, fields=fields).build()
        Leads.object.create_leads(json.loads(json_raw).get('result'))
