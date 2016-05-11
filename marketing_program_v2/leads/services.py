import ast
import json
import urllib
from urlparse import urlunparse

import requests


class BaseClient:
    def __init__(self):
        self.instance_url = ''
        self.path = ''
        self.param = ''
        self.headers = ''
        self.client_id = ''
        self.client_secret = ''

    def set_headers(self):
        token = self.get_token()
        self.headers = {'Authorization': 'Bearer ' + ast.literal_eval(token.text)["access_token"]}
        return self

    def get_token(self):
        try:
            self.path = '/identity/oauth/token'

            dict = {'grant_type': 'client_credentials', 'client_id': self.client_id,
                    'client_secret': self.client_secret}
            self.param = urllib.urlencode(dict)
            return requests.get(self)
        except requests.exceptions.RequestException as e:
            print e

    def __str__(self):
        if isinstance(self.param, dict):
            return urlunparse(("https", self.instance_url, self.path, "", urllib.urlencode(self.param), ""))
        else:
            return urlunparse(("https", self.instance_url, self.path, "", self.param, ""))

    def build(self):
        try:
            to_return = requests.get(url=self, headers=self.headers).text
            if json.loads(to_return).get('success'):
                return to_return
            else:
                return RuntimeError
        except requests.exceptions.RequestException as e:
            print(e)
            return RuntimeError


class LeadClient(BaseClient):
    def __init__(self, client_id, client_secret, instance_url, path='', param=''):
        BaseClient.__init__(self)
        self.path = path
        self.param = param
        self.client_id = client_id
        self.client_secret = client_secret
        self.instance_url = instance_url

    def with_path(self, path):
        self.set_headers()
        self.path = path
        return self

    def get_lead(self, lead_id):
        self.path = self.path.format(id=lead_id)
        return self

    def get_leads(self, filter_type, ids, fields=''):
        d = dict(filterValues=','.join(str(x) for x in ids))
        d['filterType'] = filter_type
        d['fields'] = ','.join(field for field in fields)
        self.param = d
        return self

    def with_param(self, param):
        self.param = param
        return self

        # if __name__ == '__main__':
        #         l = LeadClient()
        # print l.with_path('/rest/v1/leads/describe.json').build()
        # print l.with_path('/rest/v1/lead/{id}.json').get_lead(22).build()
        # print l.with_path('/rest/v1/leads.json').get_leads('Id', [22, 24]).build()
        # print l.with_path('/rest/v1/leads.json').get_leads('Id', [22, 24], ['company', 'site']).build()
