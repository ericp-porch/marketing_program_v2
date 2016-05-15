from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Fields, Leads


class AboutView(ListView):
    template_name = "leads/leads.html"
    context_object_name = "fields"
    model = Fields
    queryset = Fields.object.all()

    # def post(self, request):
    #     # fields = request.POST.getlist('fieldselect')
    #     return render(request, 'leads/view.html')


class LeadView(AboutView, ListView):
    template_name = "leads/view.html"
    context_object_name = "leads"
    model = Leads

    def post(self, request):
        fields = request.POST.getlist('selectfields')
        print len(fields)
        queryset = Leads.objects.all().values('document')

        return render(request, "leads/view.html", {'leads': queryset, 'fields': fields})


class FilterView(TemplateView):
    template_name = "leads/filter.html"
