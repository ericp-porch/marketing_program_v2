from __future__ import absolute_import, unicode_literals
import sys, os
reload(sys)
sys.setdefaultencoding('utf8')
import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.shortcuts import render
from django.db import connection
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
        lead_num = Leads.objects.all().count() # Total number of leads in database
        fields = request.POST.getlist('selectfields') # 'fields' is a list of rest names, from the Field table, selected by the user on leads/leads.html
        queryset = Leads.objects.all().values('document')[:100] # 'leads' is the Leads table. Check the 'queryset' variable below to see if it is limited
        FieldsEntries = Fields.object.all() # Everything from the 'Fields' database
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
        return render(request, "leads/view.html", {'leads': queryset, 'fields': fields, 'lead_num': lead_num,
                                                   'fielddata': fielddata, 'fieldtype': fieldtype})


class FilterView(LeadView, ListView):
    template_name = "leads/filter.html"
    context_object_name = "leads"
    model = Leads
    queryset = Leads.objects.all().values('document')

    def user_filters(self, request):
        fields = []
        # These 1st IF statements matches up id filter values with 'idstart' and 'idend'
        if request.POST['id_start'] == "":
            idstart = request.POST['id_start']
        else:
            idstart = int(request.POST['id_start'])
        if request.POST['id_end'] == "":
            idend = request.POST['id_end']
        else:
            idend = int(request.POST['id_end'])
        # This 'filters' dictionary will eventually contain the user-submitted filter values for the user-selected fields.
        # We now what goes with the 'id' key already.
        # The first number in the value list is an integer that marks the associated field's datatype:
        #   0 = range: These have min and max values
        #   1 = string:
        #   2 = boolean: A string reading "true", "false", or "both"
        filters = {'id': [0, idstart, idend]}  # The creation of the 'filters' dictionary
        for key, value in request.POST.items():
            if 'selectfields' in key:  # I created some hidden input elements in view.html,
                # whose names are just the rest names with 'selectfields attached.
                # This allowed me to easily get a list of field rest names right here.
                fields.append(value)
            elif '_start' in key and 'id' not in key:  # non-date ranges are converted to floatingpoint
                a = key[:-6]  # "start" is removed form the rest name, then value is made into key for 'filters' entry
                b = float(value)  # start value converted from string to float
                d = 0  # value is datatype variable index. A value of 0 indicates a range variable
                for key2, value2 in request.POST.items():
                    if a + '_end' in key2:
                        c = float(value2)  # The 'end' or max value is converted to float to be added to 'filters'
                filters.update({a: [d, b, c]})  # non-date and non-id range is added to 'filters'
            elif 'dstart' in key and 'id' not in key:  # date and datetime variables are NOT converted to floats
                a = key[:-6]
                b = value
                d = 0  # value is datatype variable index. A value of 0 indicates a range variable
                for key2, value2 in request.POST.items():
                    if a + 'dend' in key2:
                        c = value2
                filters.update({a: [d, b, c]})  # date type is added to 'filters'
            elif '_str' in key:
                filters.update({key[:-4]: [1, value]})  # the index value of "1" indicates a string variable
            elif '_boolean' in key:
                filters.update({key[:-8]: [2, value]})  # the index value of 2 "indicates a boolean variable
        return filters

    def filter_leads(self, lead, filters, counter, csvrow, csvdict):
        for key, value in lead.iteritems():
            if key == 'document':  # The 'document' JSON is accessed here
                counter += 1
                for dockey, docval in value.iteritems():  # Here is where the bulk of the filtering occurs
                    if docval:  # Some values in 'document' are null, and can't be filtered normally. This automatically disqualifies those leads
                        for filterkey, filterval in filters.iteritems():
                            if filterkey == dockey:  # Match keys between 'filters' and 'document'
                                if filterval[0] == 0:  # range variables
                                    if (filterval[1] <= docval <= filterval[2]) or (
                                            filterval[1] == filterval[2] == "") or (
                                            filterval[1] <= docval and filterval[2] == "") or (
                                            filterval[1] == "" and filterval[2] >= docval):
                                        csvrow.update({dockey: docval})
                                    else:  # if out of range, clear csvrow and kill loop
                                        csvrow.clear()
                                        return counter, csvrow, csvdict
                                elif filterval[0] == 1:  # string variables
                                    if filterval[1] in docval:
                                        csvrow.update({dockey: docval})
                                    else:  # if string does not match, clear csvrow and kill loop
                                        csvrow.clear(); return counter, csvrow, csvdict
                                elif filterval[0] == 2:
                                    if filterval[1] == docval:
                                        csvrow.update({dockey: docval})
                                    else:  # if wrong boolean value, clear csvrow and kill loop
                                        csvrow.clear(); return counter, csvrow, csvdict
                                else:  # For testing purposes only
                                    print counter, "INDEX ERROR"
                                    csvrow.clear()
                    else:
                        csvrow.clear(); return counter, csvrow, csvdict # if 'document' value is null
        # This for loop adds csvrow to csvdict. This only happens if the current lead is not filtered out.
        for key, value in csvdict.iteritems():
            for rowkey, rowval in csvrow.iteritems():
                if key == rowkey:
                    value.append(rowval)
        return counter, csvrow, csvdict

    def csv_write(self, csvdict):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sample.csv"'
        writer = csv.writer(response)
        writer.writerow(csvdict.keys())
        writer.writerows(zip(*csvdict.values()))
        return response

    def post(self, request):
        filters = self.user_filters(request)
        #
        # 'filters' is now complete. It is a dictionary where:
        # key = rest name
        # value = list[ datatype, filter_value or min_value, max_value in the case of range variable]
        #
        # idstr = "Select id, document FROM Leads WHERE (Cast(document->> 'id' AS integer) BETWEEN 500 AND 800)"
        # emailstr = "AND (document->> 'email' LIKE '%@gmail.com')"
        # final = idstr + emailstr
        # example = Leads.objects.raw(final)
        # for exam in example:
        #     print exam.id, exam.email

        # 'leader' queries the values of the 'document' column in the Leads database
        leader = Leads.objects.all().values('document')
        counter = 0 # Goes up by 1 for each lead processed
        csvdict = {} # Dictionary eventually containg the data that will be converted to a CSV
        csvrow = {} # An entry for a single lead that will be added to csvdict
        for filterkey, filterval in filters.iteritems():
            csvdict.update({filterkey: []}) # This just adds the rest names present in 'filters' to the top of csvdict, so they can be the headers for the CSV
        # Now we iterate through Leads and compare the leads to the filters to see which we keep.
        # If a single lead value is excluded by the filters, the entire lead is dumped and the the next lead is tested
        for lead in leader:
            csvrow.clear() # resets csvrow, so new lead data can be added
            counter, csvrow, csvdict = self.filter_leads(lead, filters, counter, csvrow, csvdict) #filtering of leads takes place here

        # csvdict is used to generate a CSV
        response = self.csv_write(csvdict)

        return response


