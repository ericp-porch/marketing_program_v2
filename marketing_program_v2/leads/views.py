from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from psycopg2.extras import NumericRange
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
        # 'leads' is the Leads table. Check the 'queryset' variable below to see if it is limited
        # 'fields' is a list of rest names, from the Field table, selected by the user on leads/leads.html
        # 'fieldata' is a dictionary matching user-selected field rest names with the field's associated data type (integer, string etc.)
        # 'fieldtype' Dictionary on what data types are included in 'fielddata'. The Official datatypes are condensed into 3 new types:
        #   -string--> string, email, phone, text, and url datatypes
        #   -range--> currency, float, date, datetime, and integer datatypes
        #   -bolean--> boolean datatype
        #   -dummy --> Catches any instances where none of the the above datatypes are used (errors)
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


class FilterView(LeadView, ListView):
    template_name = "leads/filter.html"
    context_object_name = "leads"
    model = Leads
    queryset = Leads.objects.all().values('document')

    def post(self, request):
        fields = []
        filters = {'id': [request.POST['id_start'], request.POST['id_end']]}
        for key, value in request.POST.items():
            if 'selectfields' in key:
                fields.append(value)
            elif '_start' in key and 'id' not in key:
                a = key[:-6]
                b = value
                d = 0 #value is a range
                for key2, value2 in request.POST.items():
                    if a +'_end' in key2:
                        c = value2
                filters.update({a:[d,b,c]})
            elif '_str' in key:
                filters.update({key[:-4]: [1,value]}) # the index value of "1" indicates a string variable
            elif '_boolean' in key:
                filters.update({key[:-8]: [2,value]}) # the index value of 2 "indicates a boolean variable
        leader = Leads.objects.all().values('document').values()
        for lead in leader:
            for key, value in lead.iteritems():
                if key == 'document':
                    for dockey, docval in value.iteritems():
                        print dockey, docval
        # x = 0
        # while x < 1:
        #     for lead in leader:
        #         print lead
        #         x += 1


        return render(request, "leads/filter.html", {'leader': leader})
