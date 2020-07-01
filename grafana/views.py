from grafana import client, models, mutators

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class OrganizationListView(PermissionRequiredMixin, ListView):
    model = models.Organization
    permission_required = "grafana.view_org"

    def get_queryset(self):
        domain = get_current_site(None).domain
        return self.model.objects.filter(apikey_set__name=domain)


class OrganizationDetailView(PermissionRequiredMixin, DetailView):
    model = models.Organization
    permission_required = "grafana.view_org"

    def get_context_data(self, **kwargs):
        context = super(OrganizationDetailView, self).get_context_data(**kwargs)
        context["dashboard_set"] = (
            models.Dashboard.objects.filter(organization=self.object)
            .prefetch_related("organization", "tag_set")
            .order_by("title")
        )
        context["version_set"] = (
            models.DashboardVersion.objects.filter(dashboard__organization=self.object)
            .prefetch_related("dashboard", "created_by")
            .order_by("-created")
        )

        if "tag" in self.request.GET:
            context["dashboard_set"] = context["dashboard_set"].filter(
                tag_set__term=self.request.GET["tag"]
            )
            context["version_set"] = context["version_set"].filter(
                dashboard__tag_set__term=self.request.GET["tag"]
            )

        # We have to do our slice last
        context["version_set"] = context["version_set"][:50]

        return context


class DashboardDetailView(PermissionRequiredMixin, DetailView):
    model = models.Dashboard
    permission_required = "grafana.view_org"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mutators"] = [driver for label, driver in mutators.Mutator.drivers()]
        return context


class DashboardMutate(PermissionRequiredMixin, DetailView):
    model = models.Dashboard
    permission_required = "grafana.view_org"
    template_name = "grafana/dashboard_mutate.html"

    def get(self, request, pk, **kwargs):
        return redirect("grafana:dash-detail", pk)

    def post(self, request, pk, **kwargs):
        for label, driver in mutators.Mutator.drivers():
            if driver.model == request.POST.get("driver"):
                break
        else:
            messages.warning(request, "Unknown driver")
            return redirect("grafana:dash-detail", pk)

        obj = self.get_object()

        if "action" in request.POST:
            client.dashboard(obj, driver.mutate(obj.json()))

        return render(
            request,
            self.template_name,
            context={
                "object": obj,
                "driver": driver,
                "output": driver.mutate(obj.json()),
            },
        )


class RevisionVersion(PermissionRequiredMixin, DetailView):
    model = models.DashboardVersion
    permission_required = "grafana.view_org"
    template_name = "grafana/version_detail.html"

