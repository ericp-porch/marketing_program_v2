from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

class Fields(models.Model):
    id = models.IntegerField("id", primary_key=True)
    display_name = models.CharField("display_name", max_length=255)
    data_type = models.CharField("data_type", max_length=255)
    length = models.IntegerField("length")
    rest_name = models.CharField("rest_name", max_length=255)
    rest_read_only = models.NullBooleanField("rest_read_only")
    soap_name = models.CharField("soapName", max_length=255)
    soap_read_only = models.NullBooleanField("soap_read_only")

    class Meta:
        db_table = "fields"


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
