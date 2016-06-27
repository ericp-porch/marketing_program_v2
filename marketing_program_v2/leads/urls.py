from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import AboutView, LeadView, FilterView

urlpatterns = (
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
