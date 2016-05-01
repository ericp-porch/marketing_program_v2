from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

class Fields(models.Model):
    id = models.IntegerField("id", primary_key=True)
    displayName = models.CharField("displayName", max_length=255)
    dataType = models.CharField("dataType", max_length=255)
    length = models.IntegerField("length")
    rest_name = models.CharField("restName", max_length=255)
    rest_read_only = models.NullBooleanField("restReadOnly")
    soap_name = models.CharField("soapName", max_length=255)
    soap_read_only = models.NullBooleanField("soapReadOnly")

    class Meta:
        db_table = "fields"


class Leads(models.Model):
    id = models.IntegerField("id", primary_key=True)
    email = models.CharField("email", max_length=255, null=True)
    updated_at = models.DateTimeField("updatedAt", null=True)
    created_at = models.DateTimeField("createdAt", null=True)
    last_name = models.CharField("lastName", max_length=255, null=True)
    first_name = models.CharField("firstName", max_length=255, null=True)
    document = JSONField("document", null=True)

    class Meta:
        db_table = "leads"
