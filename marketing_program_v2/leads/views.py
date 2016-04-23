from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "leads/leads.html"
