from __future__ import absolute_import, unicode_literals

import json

from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Leads, Fields
from .services import LeadClient


class AboutView(TemplateView):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "404.html")
        else:
            return render(request, "leads/leads.html")


class LeadView(TemplateView):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "404.html")
        else:
            return render(request, "leads/view.html")

    # def get(self, request):
    #     entries = LeadFields.objects.all()
    #     return render(request, self.template_name, {'fields': entries})

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "404.html")
        # result = request.POST.getlist('fields')
        # result_dict = {}
        # for row in result:
        #     array_f = [x.strip() for x in row.split(',')]
        #     result_dict[array_f[0]] = array_f[1]
        # json_response = get_leads(result_dict.values())
        # return JsonResponse(json_response, safe=False)
        return render(request, "post method")


class CommandView(TemplateView):
    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "404.html")

        # LIVE VERSION
        # l = LeadClient(request.user.client_id, request.user.client_secret, request.user.instance)
        # build1 = l.with_path('/rest/v1/leads/describe.json').build()
        # Fields.object.create_fields(json.loads(build1).get('result'))
        # for x in range(600, 10000, 100):
        #     range1 = range(x, x + 101)
        #     build = l.with_path('/rest/v1/leads.json').get_leads('Id', range1).build()
        #     Leads.object.create_leads(json.loads(build).get('result'))

        # FROM STATIC FILE
        # f = open('static/leads.json', 'r')
        # read = f.read()
        # Leads.object.create_leads(json.loads(read).get('result'))

        values = Leads.object.all()[:1].values('document')[0].get('document').keys()
        leads = Leads.object.all()[:100].values('document')

        return render(request, "leads/command.html", context={'leads': leads, 'values': values})

    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "404.html")
        return render(request, "leads/command.html")
