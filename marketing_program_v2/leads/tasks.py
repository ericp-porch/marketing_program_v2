from __future__ import absolute_import

import json

from marketing_program_v2.leads.models import Leads
from .celery import app
from .services import LeadClient


@app.task(name='get-leads')
def get_leads(existing_ids, fields, client_id, client_secret, instance):
    l = LeadClient(client_id, client_secret, instance)
    if not existing_ids:
        for x in range(0, 1000, 100):
            range_of_ids = range(x, x + 101)
            db_function(l, range_of_ids, fields)

    else:
        list_of_hundreds = [existing_ids[i:i + 100] for i in range(0, len(existing_ids), 100)]
        for every_list in list_of_hundreds:
            db_function(l, every_list, fields)


def db_function(l, every_list, fields):
    json_raw = l.with_path('/rest/v1/leads.json').get_leads('Id', every_list, fields=fields).build()
    # Leads.object.create_leads(json.loads(json_raw).get('result'))
