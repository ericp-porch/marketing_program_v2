from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models
import django_tables2


class FieldsManager(models.Manager):
    def create_fields(self, field_dict):
        field = self.update_or_create(id=field_dict['id'],
                                      display_name=field_dict['displayName'],
                                      data_type=field_dict['dataType'],
                                      length=field_dict['length'] if 'length' in field_dict else None,
                                      rest_name=field_dict['rest']['name'] if 'rest' in field_dict else '',
                                      rest_read_only=field_dict['rest']['readOnly'] if 'rest' in field_dict else None,
                                      soap_name=field_dict['soap']['name'] if 'soap' in field_dict else '',
                                      soap_read_only=field_dict['soap']['readOnly'] if 'soap' in field_dict else None)
        return field


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
            to_add = Leads(id=lead['id'], email=lead['email'], updated_at=lead['updatedAt'],
                           created_at=lead['createdAt'],
                           last_name=lead['lastName'], first_name=lead['firstName'], document=lead)

            if self.filter(id=to_add.id).exists():
                print 'ignore for now'
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
