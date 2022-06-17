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
        context = super().get_context_data(**kwargs)
        context["dashboard_set"] = (
            models.Dashboard.objects.filter(organization=self.object)
            .prefetch_related("organization", "tag_set")
            .order_by("title")
        )

        if "tag" in self.request.GET:
            context["dashboard_set"] = context["dashboard_set"].filter(
                tag_set__term=self.request.GET["tag"]
            )

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
            client.dashboard(obj, driver.mutate(obj.data))

        return render(
            request,
            self.template_name,
            context={
                "object": obj,
                "driver": driver,
                "output": driver.mutate(obj.data),
            },
        )


class RevisionVersion(PermissionRequiredMixin, DetailView):
    model = models.DashboardVersion
    permission_required = "grafana.view_org"
    template_name = "grafana/version_detail.html"


class VersionList(PermissionRequiredMixin, ListView):
    model = models.DashboardVersion
    permission_required = "grafana.view_org"
    template_name = "grafana/version_list.html"
    paginate_by = 100

    def get_queryset(self):
        return (
            self.model.objects.filter(dashboard__organization=self.kwargs["pk"])
            .prefetch_related("dashboard", "created_by")
            .order_by("-created")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = models.Organization.objects.get(pk=self.kwargs["pk"])
        return context


class AnnotationList(PermissionRequiredMixin, ListView):
    model = models.Annotation
    permission_required = "grafana.view_annotations"
    paginate_by = 100

    def get_queryset(self):
        return (
            self.model.objects.filter(alert_id=0, organization_id=self.kwargs["pk"])
            .prefetch_related("organization", "user")
            .order_by("-created")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = models.Organization.objects.get(pk=self.kwargs["pk"])
        return context


class UserList(PermissionRequiredMixin, ListView):
    model = models.OrgMember
    permission_required = "grafana.view_org"
    paginate_by = 100
    template_name = "grafana/organization_members.html"

    def get_queryset(self):
        return (
            self.model.objects.filter(organization_id=self.kwargs["pk"])
            .prefetch_related("organization", "user")
            .order_by("role", "user__name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = models.Organization.objects.get(pk=self.kwargs["pk"])
        return context
