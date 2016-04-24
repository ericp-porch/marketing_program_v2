from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import render


class AboutView(TemplateView):
    template_name = "leads/leads.html"


class LeadView(TemplateView):
    template_name = "leads/view.html"
# def leadview(request):
#     return render(request, 'leads/view.html')
