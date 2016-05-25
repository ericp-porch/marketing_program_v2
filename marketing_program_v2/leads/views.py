from __future__ import absolute_import, unicode_literals
import sys, os
reload(sys)
sys.setdefaultencoding('utf8')
import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.shortcuts import render
from django.views.generic import ListView
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
        fields = request.POST.getlist('selectfields') # 'fields' is a list of rest names, from the Field table, selected by the user on leads/leads.html
        queryset = Leads.objects.all().values('document')[:100] # 'leads' is the Leads table. Check the 'queryset' variable below to see if it is limited
        FieldsEntries = Fields.object.all()
        datatypes = []
        for field in fields:
            for entry in FieldsEntries:
                if field == entry.rest_name:
                    datatypes.append(entry.data_type)
        fielddata = dict(zip(fields, datatypes)) # 'fieldata' is a dictionary matching user-selected field rest names with the field's associated data type (integer, string etc.)
        string, range, boolean, dummy = 0,0,0,0
        for field, datatype in fielddata.iteritems():
            if datatype in "string email phone text url":
                string += 1 # string--> string, email, phone, text, and url datatypes
            elif datatype in "currency float date datetime integer":
                range += 1 # range--> currency, float, date, datetime, and integer datatypes
            elif datatype == "boolean":
                boolean += 1 # bolean--> boolean datatype
            else:
                dummy += 1 # dummy --> Catches any instances where none of the the above datatypes are used (errors)
        fieldtype = {"string":string, "range":range, "boolean":boolean, "dummy":dummy} # 'fieldtype' Dictionary on what data types are included in 'fielddata'. The Official datatypes are condensed into 3 new types:
        return render(request, "leads/view.html", {'leads': queryset, 'fields': fields, 'fielddata': fielddata, 'fieldtype': fieldtype})


class FilterView(LeadView, ListView):
    template_name = "leads/filter.html"
    context_object_name = "leads"
    model = Leads
    queryset = Leads.objects.all().values('document')

    def post(self, request):
        fields = []
        if request.POST['id_start'] == "":
            idstart = request.POST['id_start']
        else: idstart = int(request.POST['id_start'])
        if request.POST['id_end'] == "":
            idend = request.POST['id_end']
        else:
            idend = int(request.POST['id_end'])

        filters = {'id': [0, idstart, idend]}
        for key, value in request.POST.items():
            if 'selectfields' in key:
                fields.append(value)
            elif '_start' in key and 'id' not in key: # non-date ranges are converted to floatingpoint
                a = key[:-6]
                b = float(value)
                d = 0 # value is datatype variable index. A value of 0 indicates a range variable
                for key2, value2 in request.POST.items():
                    if a +'_end' in key2:
                        c = float(value2)
                filters.update({a:[d,b,c]})
            elif 'dstart' in key and 'id' not in key: # date and datetime variables
                a = key[:-6]
                b = value
                d = 0  # value is datatype variable index. A value of 0 indicates a range variable
                for key2, value2 in request.POST.items():
                    if a + 'dend' in key2:
                        c = value2
                filters.update({a: [d, b, c]})
            elif '_str' in key:
                filters.update({key[:-4]: [1,value]}) # the index value of "1" indicates a string variable
            elif '_boolean' in key:
                filters.update({key[:-8]: [2,value]}) # the index value of 2 "indicates a boolean variable
        leader = Leads.objects.all().values('document').values()
        counter = 0
        csvdict = {}
        csvrow = {}
        for filterkey, filterval in filters.iteritems():
            csvdict.update({filterkey: [""]})
        for lead in leader:
            loopstatus = 0
            csvrow.clear()
            while loopstatus == 0:
                for key, value in lead.iteritems():
                    if key == 'document':
                        counter += 1
                        for dockey, docval in value.iteritems():
                            if docval:
                                for filterkey, filterval in filters.iteritems():
                                    if filterkey == dockey:
                                        if filterval[0] == 0:
                                            if (filterval[1] <= docval <= filterval[2]) or (filterval[1] == filterval[2] == "") or (filterval[1] <= docval and filterval[2] == "") or (filterval[1] == "" and filterval[2] >= docval):
                                                csvrow.update({dockey: docval})
                                            else:
                                                csvrow.clear()
                                                print counter, filterkey, filterval, docval
                                                loopstatus = 1
                                        elif filterval[0] == 1:
                                            if filterval[1] in docval or filterval[1] == "":
                                                csvrow.update({dockey: docval})
                                            else:
                                                print counter, filterkey
                                                csvrow.clear()
                                                loopstatus = 1
                                        elif filterval[0] == 2:
                                            if filterval[1] == docval or (filterval[1] == ""):
                                                csvrow.update({dockey: docval})
                                            else:
                                                csvrow.clear()
                                                print counter, filterkey
                                                loopstatus = 1
                                        else:
                                            print counter, "INDEX ERROR"
                                            csvrow.clear()
                            else: csvrow.clear(); loopstatus = 1
                for key, value in csvdict.iteritems():
                    for rowkey, rowval in csvrow.iteritems():
                        if key == rowkey:
                            value.append(rowval)
                loopstatus = 1

        keys = csvdict.keys()
        sep = b","
        with open("/Users/kennethharmon/marketing_program_v2/marketing_program_v2/templates/leads/test.csv", "wb") as outfile:
            writer = csv.writer(outfile, delimiter=sep)
            writer.writerow(keys)
            writer.writerows(zip(*[csvdict[key] for key in keys]))

        return render(request, "leads/filter.html", {"csvdict": csvdict})


