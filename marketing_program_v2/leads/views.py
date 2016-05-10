from __future__ import absolute_import, unicode_literals

import json

from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Fields, Leads
from .services import LeadClient


class AboutView(TemplateView):
    template_name = "leads/leads.html"


class LeadView(TemplateView):
    template_name = "leads/view.html"

    # def get(self, request):
    #     entries = LeadFields.objects.all()
    #     return render(request, self.template_name, {'fields': entries})

    def post(self, request):
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
            return HttpResponseForbidden()
        # l = LeadClient()
        # range1 = range(300, 401)
        # build = l.with_path('/rest/v1/leads.json').get_leads('Id', range1).build()
        # Leads.object.create_leads(json.loads(build).get('result'))

        # f = open('static/leads.json', 'r')
        # read = f.read()
        # Leads.object.create_leads(json.loads(read).get('result'))

        leads = Leads.object.all()
        return render(request, "leads/command.html", context={'leads': leads})

    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        return render(request, "leads/command.html")
