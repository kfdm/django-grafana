from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from grafana import models


class OrganizationListView(ListView):
    model = models.Organization


class OrganizationDetailView(DetailView):
    model = models.Organization

    def get_context_data(self, **kwargs):
        context = super(OrganizationDetailView, self).get_context_data(**kwargs)
        context['dashboard_set'] = models.Dashboard.objects\
            .filter(orginization=self.object)\
            .prefetch_related('orginization', 'tag_set').order_by('title')
        context['version_set'] = models.DashboardVersion.objects\
            .filter(dashboard__orginization=self.object)\
            .prefetch_related('dashboard', 'created_by')
        return context


class DashboardDetailView(DetailView):
    model = models.Dashboard
