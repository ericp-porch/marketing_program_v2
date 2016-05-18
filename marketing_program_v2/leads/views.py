from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Fields, Leads


class AboutView(ListView):
    template_name = "leads/leads.html"
    context_object_name = "fields"
    model = Fields
    queryset = Fields.object.all()


class LeadView(AboutView, ListView):
    template_name = "leads/view.html"
    context_object_name = "leads"
    model = Leads

    def post(self, request):

        fields = request.POST.getlist('selectfields')
        queryset = Leads.objects.all().values('document')[:100]
        FieldsEntries = Fields.object.all()
        datatypes = []
        for field in fields:
            for entry in FieldsEntries:
                if field == entry.rest_name:
                    datatypes.append(entry.data_type)
        fielddata = dict(zip(fields, datatypes))
        string, range, boolean, dummy = 0,0,0,0
        for field, datatype in fielddata.iteritems():
            if datatype in "string email phone text url":
                string += 1
            elif datatype in "currency float date datetime integer":
                range += 1
            elif datatype == "boolean":
                boolean += 1
            else:
                dummy += 1
        fieldtype = {"string":string, "range":range, "boolean":boolean, "dummy":dummy}
        return render(request, "leads/view.html", {'leads': queryset, 'fields': fields, 'fielddata': fielddata, 'fieldtype': fieldtype})


class FilterView(TemplateView):
    template_name = "leads/filter.html"
