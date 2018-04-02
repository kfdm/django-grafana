from grafana import models

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class OrganizationListView(PermissionRequiredMixin, ListView):
    model = models.Organization
    permission_required = 'grafana.view_org'

    def get_queryset(self):
        return self.model.objects.filter(apikey_set__name='django')


class OrganizationDetailView(PermissionRequiredMixin, DetailView):
    model = models.Organization
    permission_required = 'grafana.view_org'

    def get_context_data(self, **kwargs):
        context = super(OrganizationDetailView, self).get_context_data(**kwargs)
        context['dashboard_set'] = models.Dashboard.objects\
            .filter(organization=self.object)\
            .prefetch_related('organization', 'tag_set').order_by('title')
        context['version_set'] = models.DashboardVersion.objects\
            .filter(dashboard__organization=self.object)\
            .prefetch_related('dashboard', 'created_by')\
            .order_by('-created')

        if 'tag' in self.request.GET:
            context['dashboard_set'] = context['dashboard_set'].filter(
                tag_set__term=self.request.GET['tag']
            )
            context['version_set'] = context['version_set'].filter(
                dashboard__tag_set__term=self.request.GET['tag']
            )


        # We have to do our slice last
        context['version_set'] = context['version_set'][:50]

        return context


class DashboardDetailView(PermissionRequiredMixin, DetailView):
    model = models.Dashboard
    permission_required = 'grafana.view_org'
