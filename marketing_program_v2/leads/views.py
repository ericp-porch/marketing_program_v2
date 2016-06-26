from __future__ import absolute_import, unicode_literals

import csv
import json
import sys

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from marketing_program_v2.leads.services import LeadClient
from marketing_program_v2.tasks import get_leads
from .models import Fields, Leads

reload(sys)
sys.setdefaultencoding('utf8')


class AboutView(ListView):
    template_name = "leads/leads.html"
    context_object_name = "fields"
    model = Fields
    queryset = Fields.object.all()


# class CustomFieldForm(FormView):
#     def get(self, request):
#         # if "save_fields" in request.GET:
#         print "success"
#         return render(request, "leads/leads.html")


class LeadView(AboutView, ListView):
    template_name = "leads/view.html"
    context_object_name = "leads"
    model = Leads

    def datatype_retrieval(self, request):
        lead_num = Leads.object.all().count()  # Total number of leads in database
        ids = Leads.object.values('id')
        existing_ids = [id['id'] for id in ids]
        fields = request.POST.getlist('selectfields')  # 'fields' is a list of user-selected rest names
        fields.insert(0, "id")

        # result = get_leads.delay(existing_ids, fields, request.user.client_id, request.user.client_secret, request.user.instance) # LIVE DON'T UNCOMMENT
        # l = LeadClient(request.user.client_id, request.user.client_secret, request.user.instance)
        #
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
        request.session['fielddata'] = fielddata
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

        filters = {'id': [idstart, idend]}  # The creation of the 'filters' dictionary
        for key, value in request.POST.items():
            if 'selectfields' in key:  # Rest Names taken from hiiden input fields
                fields.append(value)
            elif '_start' in key and 'id' not in key:  # non-date ranges are converted to floats
                a = key[:-6]  # "start" is removed form the rest name, then value is made into key for 'filters' entry
                if value == "":
                    b = value
                else:
                    b = float(value)  # start value converted from string to float
                for key2, value2 in request.POST.items():
                    if a + '_end' in key2:
                        if value2 == "":
                            c = value2
                        else:
                            c = float(value2)  # The 'end' or max value is converted to float to be added to 'filters'
                filters.update({a: [b, c]})  # non-date and non-id range is added to 'filters'
            elif 'dstart' in key and 'id' not in key:  # date and datetime variables are NOT converted to floats
                a = key[:-6]
                b = value
                for key2, value2 in request.POST.items():
                    if a + 'dend' in key2:
                        c = value2
                filters.update({a: [b, c]})  # date type is added to 'filters'
            elif '_str' in key:
                filters.update({key[:-4]: value})
            elif '_boolean' in key:
                filters.update({key[:-8]: value})
        return filters, fields

    def object_create(self, key, object_list):
        object_part = "'" + key + "', document ->> '" + key + "'"
        object_list.append(object_part)
        return object_list

    def range_filter(self, key, value, param, querySTR, data_type, filter_clause):
        if value[0] == "" and value[1] == "":
            pass
        elif value[1] != "" and value[1] != "":
            param.append(value[0])
            param.append(value[1])
            paramSTR = "CAST(document->>'" + key + "' AS " + data_type + " ) BETWEEN %s AND %s "
            querySTR.append(paramSTR)
            filter_clause = 1
        elif value[0] != "" and value[1] == "":
            param.append(value[1])
            paramSTR = "CAST(document->>'" + key + "' AS " + data_type + " ) < %s "
            querySTR.append(paramSTR)
            filter_clause = 1
        elif value[0] == "" and value[1] != "":
            param.append(value[1])
            paramSTR = "CAST(document->>'" + key + "' AS " + data_type + " ) < %s "
            querySTR.append(paramSTR)
            filter_clause = 1
        return param, querySTR, filter_clause

    def SQL_filter(self, filters, fielddata):
        object_list, param, querySTR, querySQL = [], [], [], []
        filter_clause = 0
        selectSTR = "SELECT id, JSONB_BUILD_OBJECT( "
        selectSTR2 = ") AS JSONDOC FROM leads WHERE "
        for key, value in filters.iteritems():
            object_list = self.object_create(key, object_list)
            if fielddata[key] in "integer":
                data_type = "integer"
                param, querySTR, filter_clause = self.range_filter(key, value, param, querySTR, data_type,
                                                                   filter_clause)
            elif fielddata[key] in "currency float":
                data_type = "float"
                param, querySTR, filter_clause = self.range_filter(key, value, param, querySTR, data_type,
                                                                   filter_clause)
            elif fielddata[key] in "date datetime":
                data_type = "date"
                param, querySTR, filter_clause = self.range_filter(key, value, param, querySTR, data_type,
                                                                   filter_clause)
            elif fielddata[key] in "string email phone text url":
                if value == "":
                    pass
                else:
                    string_param = "%%" + value + "%%"
                    param.append(string_param)
                    paramSTR = "document->>'" + key + "' ILIKE %s"
                    querySTR.append(paramSTR)
                    filter_clause = 1
            elif fielddata[key] in "boolean":
                if value == "both":
                    pass
                elif value == "true":
                    paramSTR = "CAST(document->>'" + key + "' AS boolean) = TRUE "
                    querySTR.append(paramSTR)
                    filter_clause = 1
                elif value == "false":
                    paramSTR = "CAST(document->>'" + key + "' AS boolean) = FALSE "
                    querySTR.append(paramSTR)
                    filter_clause = 1
        sqlSTR = "AND ".join(querySTR)
        objectSTR = ",".join(object_list)
        cursor = connection.cursor()
        if filter_clause == 0:
            selectSTR2 = ") AS JSONDOC FROM leads "
            finalSTR = selectSTR + objectSTR + selectSTR2
            cursor.execute(finalSTR)
            csvdata = cursor.fetchall()
        elif filter_clause == 1:
            selectSTR2 = ") AS JSONDOC FROM leads WHERE "
            finalSTR = selectSTR + objectSTR + selectSTR2 + sqlSTR
            cursor.execute(finalSTR, param)
            csvdata = cursor.fetchall()
        return csvdata

    def csv_write(self, csvdata, filters):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sample.csv"'
        writer = csv.writer(response)
        if not csvdata:
            writer.writerow(filters.keys())
        else:
            writer.writerow(csvdata[1][1].keys())
            for row in csvdata:
                writer.writerow(row[1].values())
        return response

    def post(self, request):
        filters, fields = self.user_filters(request)
        fielddata = request.session['fielddata']
        csvdata = self.SQL_filter(filters, fielddata)
        response = self.csv_write(csvdata, filters)

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
