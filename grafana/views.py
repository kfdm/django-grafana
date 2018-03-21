from django.http import HttpResponse
from django.views import View

from django.views.generic.list import ListView
from django.utils import timezone
from django.views.generic.detail import DetailView

from grafana import models


class OrganizationListView(ListView):
    model = models.Organization


class OrganizationDetailView(DetailView):
    model = models.Organization


class DashboardDetailView(DetailView):
    model = models.Dashboard
