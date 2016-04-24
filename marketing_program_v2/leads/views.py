from __future__ import absolute_import, unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
import json
from .models import Fields

from .services import LeadClient


class AboutView(TemplateView):
    # l = LeadClient()
    # build = l.with_path('/rest/v1/leads/describe.json').build()
    # list = range(1, 101)
    # print list
    # print l.with_path('/rest/v1/leads.json').get_leads('Id', list, ['company', 'site']).build()

    # response = json.load(open('lead_fields.json'))
    # for field in response['result']:
    #     Fields.object.create_fields(field)

    # f = open('lead_fields.json', 'w')
    # f.write(build)
    template_name = "leads/leads.html"


class LeadView(TemplateView):
    template_name = "leads/view.html"

    def get(self, request):
        entries = LeadFields.objects.all()
        return render(request, self.template_name, {'fields': entries})

    def post(self, request):
        # result = request.POST.getlist('fields')
        # result_dict = {}
        # for row in result:
        #     array_f = [x.strip() for x in row.split(',')]
        #     result_dict[array_f[0]] = array_f[1]
        # json_response = get_leads(result_dict.values())
        # return JsonResponse(json_response, safe=False)
        return render(request,"post method")

# def leadview(request):
#     return render(request, 'leads/view.html')
