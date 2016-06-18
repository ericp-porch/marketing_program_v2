from __future__ import absolute_import, unicode_literals

import sys

from marketing_program_v2.leads.services import LeadClient

import csv
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Fields, Leads
import json
reload(sys)
sys.setdefaultencoding('utf8')


class AboutView(ListView):
    template_name = "leads/leads.html"
    context_object_name = "fields"
    model = Fields
    queryset = Fields.object.all()


class LeadView(AboutView, ListView):
    template_name = "leads/view.html"
    context_object_name = "leads"
    model = Leads

    def datatype_retrieval(self, request):
        lead_num = Leads.object.all().count()  # Total number of leads in database
        fields = request.POST.getlist('selectfields')  # 'fields' is a list of user-selected rest names
        l = LeadClient(request.user.client_id, request.user.client_secret, request.user.instance)

        # for x in range(0, 300, 100):
        #     range_of_ids = range(x, x + 101)
        #     json_raw = l.with_path('/rest/v1/leads.json').get_leads('Id', range_of_ids, fields=fields).build()
        #     Leads.object.create_leads(json.loads(json_raw).get('result'))

        queryset = Leads.object.all().values('document')[:100]  # 'leads' is the Leads table.
        FieldsEntries = Fields.object.all()  # Everything from the 'Fields' database
        datatypes = []
        for field in fields:
            for entry in FieldsEntries:
                if field == entry.rest_name:
                    datatypes.append(entry.data_type)
        return lead_num, fields, queryset, datatypes

    def data_sort(self, request, fields, datatypes):
        fielddata = dict(zip(fields, datatypes))  # 'fieldata' is a dictionary with fields and associated data type
        request.session['fielddata']=fielddata
        string, range1, boolean, dummy = 0, 0, 0, 0
        for field, datatype in fielddata.iteritems():
            if datatype in "string email phone text url":
                string += 1  # string--> string, email, phone, text, and url datatypes
            elif datatype in "currency float date datetime integer":
                range1 += 1  # range--> currency, float, date, datetime, and integer datatypes
            elif datatype == "boolean":
                boolean += 1  # boolean--> boolean datatype
            else:
                dummy += 1  # errors
        # 'fieldtype' Dictionary on what data types are included in 'fielddata'.
        fieldtype = {"string": string, "range": range1, "boolean": boolean, "dummy": dummy}
        return fieldtype, fielddata

    def table_fill(self, fielddata, queryset):
        tabledict = {'id': []}
        tablelist = ['id']
        for field, datatype in fielddata.iteritems():
            if field != "id":
                tablelist.append(field)
                tabledict.update({field: []})
        for header in tablelist:
            for lead in queryset:
                for json, document in lead.iteritems():
                    if header in document:
                        tabledict[header].append(document[header])
                    else:
                        tabledict[header].append("---")
                    for key, val in document.iteritems():
                        if key == header:
                            tabledict[header].append(val)
        return tabledict, tablelist

    def post(self, request):
        if "get_leads" in request.POST:
            lead_num, fields, queryset, datatypes = self.datatype_retrieval(request)
            fieldtype, fielddata = self.data_sort(request, fields, datatypes)
            tabledict, tablelist = self.table_fill(fielddata, queryset)
            return render(request, "leads/view.html", {'leads': queryset, 'fields': fields, 'lead_num': lead_num,
                                                       'fielddata': fielddata, 'fieldtype': fieldtype,
                                                       'tablelist': tablelist, 'tabledict': tabledict})
        elif "saveSubmit" in request.POST:
            template_name = "leads/leads.html"
            return render(request, "leads/leads.html")


class FilterView(LeadView, ListView):
    template_name = "leads/filter.html"
    context_object_name = "leads"
    model = Leads
    queryset = Leads.object.all().values('document')

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
            if 'selectfields' in key:  # Rest Names taken from hiiden input fields
                fields.append(value)
            elif '_start' in key and 'id' not in key:  # non-date ranges are converted to floats
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
        return filters, fields

    def filter_out(self, fields, dockey):
        for field in fields:
            if dockey == field:
                filterout = 0
            else:
                filterout = 1
                return filterout
        return filterout

    def filter_leads(self,leader, filters, counter, csvrow, csvdict, fields):
        for lead in leader:
            csvrow.clear()
            for key, value in lead.iteritems():
                if key == 'document':  # The 'document' JSON is accessed here
                    counter += 1
                    for dockey, docval in value.iteritems():  # Here is where the bulk of the filtering occurs
                        filterout = self.filter_out(fields, dockey)
                        if filterout == 1:
                            csvrow.clear()
                            return counter, csvrow, csvdict
                        else:
                            print counter, dockey, docval
                            if docval:  # Leads with null values are filtered out
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
                                                csvrow.clear();
                                                return counter, csvrow, csvdict
                                        elif filterval[0] == 2:
                                            if filterval[1] == docval or filterval[1] in "both":
                                                csvrow.update({dockey: docval})
                                            else:  # if wrong boolean value, clear csvrow and kill loop
                                                csvrow.clear();
                                                return counter, csvrow, csvdict
                                        else:  # For testing purposes only
                                            print counter, "INDEX ERROR"
                                            csvrow.clear()
                            else:
                                csvrow.clear();
                                return counter, csvrow, csvdict  # if 'document' value is null
        for key, value in csvdict.iteritems():  # If lead not filtered out, csvrow is added to csvdict
            for rowkey, rowval in csvrow.iteritems():
                if key == rowkey:
                    value.append(rowval)
        return counter, csvrow, csvdict

    def csv_write(self, csvdict):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sample.csv"'
        writer = csv.writer(response)
        writer.writerow(csvdict[1][1].keys())
        for row in csvdict:
            writer.writerow(row[1].values())
        # writer.writerows(zip(*csvdict.values()))
        return response


    def SQL_filter(self, filters, fielddata):
        object_list, param, querySTR, querySQL = [], [], [], []
        filter_clause = 0
        # selectSTR = "SELECT id, document FROM leads WHERE "
        selectSTR = "SELECT id, JSONB_BUILD_OBJECT( "
        selectSTR2 = ") AS JSONDOC FROM leads WHERE "
        for key, value in filters.iteritems():
            object_part = "'" + key + "', document ->> '" + key +"'"
            object_list.append(object_part)
            if fielddata[key] in "integer":
                if value[1] == "" and value[2] == "":
                    pass
                elif value[1] != "" and value[2] != "":
                    param.append(value[1])
                    param.append(value[2])
                    paramSTR = "CAST(document->>'" + key + "' AS integer) BETWEEN %s AND %s "
                    querySTR.append(paramSTR)
                    filter_clause = 1
                elif value[1] != "" and value[2] == "":
                    param.append(value[1])
                    paramSTR = "CAST(document->>'" + key + "' AS integer) < %s "
                    querySTR.append(paramSTR)
                    filter_clause = 1
                elif value[1] == "" and value[2] != "":
                    param.append(value[2])
                    paramSTR = "CAST(document->>'" + key + "' AS integer) < %s "
                    querySTR.append(paramSTR)
                    filter_clause = 1
            elif fielddata[key] in "currency float":
                if value[1] == "" and value[2] == "":
                    pass
                elif value[1] != "" and value[2] != "":
                    param.append(value[1])
                    param.append(value[2])
                    paramSTR = "CAST(document->>'" + key + "' AS float) BETWEEN %s AND %s "
                    querySTR.append(paramSTR)
                    filter_clause = 1
                elif value[1] != "" and value[2] == "":
                    param.append(value[1])
                    paramSTR = "CAST(document->>'" + key + "' AS float) < %s "
                    querySTR.append(paramSTR)
                    filter_clause = 1
                elif value[1] == "" and value[2] != "":
                    param.append(value[2])
                    paramSTR = "CAST(document->>'" + key + "' AS float) < %s "
                    querySTR.append(paramSTR)
                    filter_clause = 1
            elif fielddata[key] in "date datetime":
                if value[1] == "" and value[2] == "":
                    pass
                elif value[1] != "" and value[2] != "":
                    param.append(value[1])
                    param.append(value[2])
                    paramSTR = "CAST(document->>'" + key + "' AS date) BETWEEN %s AND %s "
                    querySTR.append(paramSTR)
                    filter_clause = 1
                elif value[1] != "" and value[2] == "":
                    param.append(value[1])
                    paramSTR = "CAST(document->>'" + key + "' AS date) < %s "
                    querySTR.append(paramSTR)
                    filter_clause = 1
                elif value[1] == "" and value[2] != "":
                    param.append(value[2])
                    paramSTR = "CAST(document->>'" + key + "' AS date) < %s "
                    querySTR.append(paramSTR)
                    filter_clause = 1
            elif fielddata[key] in "string email phone text url":
                if value[1] == "":
                    pass
                else:
                    string_param = "%%" + value[1] + "%%"
                    param.append(string_param)
                    paramSTR = "document->>'" + key + "' ILIKE %s"
                    querySTR.append(paramSTR)
                    filter_clause = 1
            elif fielddata[key] in "boolean":
                if value[1] == "both":
                    pass
                elif value[1] == "true":
                    paramSTR = "document->>'" + key + "' is true"
                    querySTR.append(paramSTR)
                    filter_clause = 1
                elif value[1] == "false":
                    paramSTR = "document->>'" + key + "' is false"
                    querySTR.append(paramSTR)
                    filter_clause = 1
        sqlSTR = "AND ".join(querySTR)
        objectSTR = ",".join(object_list)
        cursor = connection.cursor()
        if filter_clause == 0:
            selectSTR2 = ") AS JSONDOC FROM leads "
            finalSTR = selectSTR + objectSTR + selectSTR2
            cursor.execute(finalSTR)
            queryFIN = cursor.fetchall()
        elif filter_clause == 1:
            selectSTR2 = ") AS JSONDOC FROM leads WHERE "
            finalSTR = selectSTR + objectSTR + selectSTR2 + sqlSTR
            print finalSTR
            cursor.execute(finalSTR, param)
            queryFIN = cursor.fetchall()
        return queryFIN


    def post(self, request):
        # filters is dict where: key= rest_name, value= [ datatype, filter_value or min_value, max_value if range]
        filters, fields = self.user_filters(request)
        fielddata = request.session['fielddata']

        leader = Leads.object.all().values('document')
        counter, csvdict, csvrow = 0, {}, {}
        for filterkey, filterval in filters.iteritems():
            csvdict.update({filterkey: []})  # filterkeys become headers for CSV
        queryFIN = self.SQL_filter(filters, fielddata)
        counter, csvrow, csvdict = self.filter_leads(leader, filters, counter, csvrow, csvdict, fields)
        response = self.csv_write(queryFIN)

        return response


class CommandView(TemplateView):
    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "404.html")

        # LIVE VERSION
        l = LeadClient(request.user.client_id, request.user.client_secret, request.user.instance)
        build1 = l.with_path('/rest/v1/leads/describe.json').build()
        Fields.object.create_fields(json.loads(build1).get('result'))
        # for x in range(600, 10000, 100):
        #     range_of_ids = range(x, x + 101)
        #     json_raw = l.with_path('/rest/v1/leads.json').get_leads('Id', range_of_ids).build()
        #     Leads.object.create_leads(json.loads(json_raw).get('result'))

        # FROM STATIC FILE
        # f = open('static/leads.json', 'r')
        # read = f.read()
        # Leads.object.create_leads(json.loads(read).get('result'))

        values = Leads.object.all()[:1].values('document')[0].get('document').keys()
        leads = Leads.object.all()[:100].values('document')

        return render(request, "leads/command.html", context={'leads': leads, 'values': values})

    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "404.html")
        return render(request, "leads/command.html")
