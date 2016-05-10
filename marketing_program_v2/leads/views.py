from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView, ListView
from .models import Fields


class AboutView(ListView):
    template_name = "leads/leads.html"
    context_object_name = "fields"
    model = Fields
    queryset = Fields.object.all()


class LeadView(TemplateView):
    template_name = "leads/view.html"


