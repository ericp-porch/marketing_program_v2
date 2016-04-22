from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    # URL pattern for the UserListView
    url(
        r'^', TemplateView.as_view(template_name='pages/leads.html'), name="home"
    ),
]
