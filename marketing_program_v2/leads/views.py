from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Fields


class AboutView(ListView):
    template_name = "leads/leads.html"
    context_object_name = "fields"
    model = Fields
    queryset = Fields.object.all()

    def post(self, request):
        fields = request.POST.getlist('fieldselect')
        return render(request, 'leads/filter.html', {'fields': fields})


class FilterView( AboutView, TemplateView):
    template_name = "leads/filter.html"



class LeadView(TemplateView):
    template_name = "leads/view.html"



