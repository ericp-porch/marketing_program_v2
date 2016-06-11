from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models


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


class LeadsManager(models.Manager):
    def create_leads(self, leads):
        objs = []
        for lead in leads:
            to_add = Leads(id=lead['id'],
                           email=lead['email'] if 'email' in lead else None,
                           updated_at=lead['updatedAt'] if 'updatedAt' in lead else None,
                           created_at=lead['createdAt'] if 'createdAt' in lead else None,
                           last_name=lead['lastName'] if 'lastName' in lead else None,
                           first_name=lead['firstName'] if 'firstName' in lead else None,
                           document=lead)

            existing_lead = self.filter(id=to_add.id)
            if existing_lead.exists():
                existing_lead.update(email=lead['email'] if 'email' in lead else None,
                                     updated_at=lead['updatedAt'] if 'updatedAt' in lead else None,
                                     created_at=lead['createdAt'] if 'createdAt' in lead else None,
                                     last_name=lead['lastName'] if 'lastName' in lead else None,
                                     first_name=lead['firstName'] if 'firstName' in lead else None,
                                     document=lead)
            else:
                objs.append(to_add)

        self.bulk_create(objs)


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
