from __future__ import absolute_import, unicode_literals

import json

from django.contrib.postgres.fields import JSONField
from django.db import models, connection


class FieldsManager(models.Manager):
    def create_fields(self, fields):
        fields_to_add = []
        for field_dict in fields:
            field = Fields(id=field_dict['id'],
                           display_name=field_dict['displayName'],
                           data_type=field_dict['dataType'],
                           length=field_dict['length'] if 'length' in field_dict else None,
                           rest_name=field_dict['rest']['name'] if 'rest' in field_dict else '',
                           rest_read_only=field_dict['rest'][
                               'readOnly'] if 'rest' in field_dict else None,
                           soap_name=field_dict['soap']['name'] if 'soap' in field_dict else '',
                           soap_read_only=field_dict['soap'][
                               'readOnly'] if 'soap' in field_dict else None)
            self_filter = self.filter(id=field.id)
            if self_filter.exists():
                self_filter.update(display_name=field_dict['displayName'],
                                   data_type=field_dict['dataType'],
                                   length=field_dict['length'] if 'length' in field_dict else None,
                                   rest_name=field_dict['rest']['name'] if 'rest' in field_dict else '',
                                   rest_read_only=field_dict['rest'][
                                       'readOnly'] if 'rest' in field_dict else None,
                                   soap_name=field_dict['soap']['name'] if 'soap' in field_dict else '',
                                   soap_read_only=field_dict['soap'][
                                       'readOnly'] if 'soap' in field_dict else None)
            else:
                fields_to_add.append(field)
        self.bulk_create(fields_to_add)


class Fields(models.Model):
    id = models.IntegerField("id", primary_key=True)
    display_name = models.CharField("display_name", max_length=255)
    data_type = models.CharField("data_type", max_length=255)
    length = models.IntegerField("length", null=True)
    rest_name = models.CharField("rest_name", max_length=255, blank=True)
    rest_read_only = models.NullBooleanField("rest_read_only")
    soap_name = models.CharField("soapName", max_length=255, blank=True)
    soap_read_only = models.NullBooleanField("soap_read_only")

    class Meta:
        db_table = "fields"

    object = FieldsManager()


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class LeadsManager(models.Manager):
    def create_leads(self, leads):
        cursor = connection.cursor()
        for lead in leads:
            default_keys = {'email': 'email', 'updatedAt': 'updated_at', 'createdAt': 'created_at',
                            'firstName': 'first_name', 'lastName': 'last_name'}
            default_values = {}
            json_values = {}
            for key, value in lead.iteritems():
                if key in default_keys:
                    default_values[default_keys[key]] = value
            obj, created = Leads.object.update_or_create(id=lead['id'], defaults=default_values)

            # if created:
            #     dict_todo = {}
            #     for key, value in lead.iteritems():
            #         dict_todo[str(key)] = str(value).replace("'", "")
            #     cursor.execute(
            #         '''UPDATE leads SET document = '{0}' WHERE id = {1} '''.format(json.dumps(dict_todo), obj.id))
            # else:
            #     for key, value in lead.iteritems():
            #         cursor.execute(
            #             '''UPDATE leads SET document = jsonb_set(document, '{{{0}}}', '"{1}"') WHERE id = {2}'''.format(
            #                 key, str(value).replace("'", ""), obj.id))
            #

class Leads(models.Model):
    id = models.IntegerField("id", primary_key=True)
    email = models.CharField("email", max_length=255, null=True)
    updated_at = models.DateTimeField("updated_at", null=True)
    created_at = models.DateTimeField("created_at", null=True)
    last_name = models.CharField("last_name", max_length=255, null=True)
    first_name = models.CharField("first_name", max_length=255, null=True)
    document = JSONField("document", null=True)

    class Meta:
        db_table = "leads"

    object = LeadsManager()
