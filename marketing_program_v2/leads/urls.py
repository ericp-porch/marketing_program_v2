from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import AboutView, LeadView, FilterView
urlpatterns = (
    # URL pattern for the UserListView
    # url(
    #     r'^', TemplateView.as_view(template_name='pages/leads.html'), name="home"
    # ),
    url(
        r'^$', AboutView.as_view(), name="home"
    ),
    url(
        r'^view/', LeadView.as_view(), name="view"
    ),
    url(
        r'^filter/', FilterView.as_view(), name="filter"
    ),
)
