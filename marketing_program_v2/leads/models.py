from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# @python_2_unicode_compatible
# class LeadFields():
#     id = models.IntegerField("id")
#     displayName = models.CharField("displayName", blank=True, max_length=255)
#     dataType = models.CharField("dataType", blank=True, max_length=255)
#     length = models.IntegerField("length")
#
#     def __str__(self):
#         return self.dataType
#
#     def get_absolute_url(self):
#         return reverse('leads:detail', kwargs={'dataTyoe': self.dataType})
