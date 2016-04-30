from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import render
from .models import LeadFields


class AboutView(TemplateView):
    template_name = "leads/leads.html"


class LeadView(TemplateView):
    template_name = "leads/view.html"
    # LIVE VERSION
    entries = LeadFields.objects.all()
    def get(self, request):
        return render(request, self.template_name, {'fields': entries})
    def post(self, request):
        result = request.POST.getlist('fields')
        result_dict = {}
        for row in result:
            array_f = [x.strip() for x in row.split(',')]
            result_dict[array_f[0]] = array_f[1]
        json_response = get_leads(result_dict.values())
        return JsonResponse(json_response, safe=False)
# def leadview(request):
#     return render(request, 'leads/view.html')


