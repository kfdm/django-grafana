from grafana import views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.OrganizationListView.as_view(), name='org-list'),
    url(r'^org/(?P<pk>.*)$', views.OrganizationDetailView.as_view(), name='org-detail'),
    url(r'^dash/(?P<pk>.*)$', views.DashboardDetailView.as_view(), name='dash-detail'),
]
