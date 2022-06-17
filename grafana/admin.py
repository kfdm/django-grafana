from django.contrib import admin
from grafana import models
import datetime


@admin.register(models.DataSource)
class DatasourceAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "type")
    list_filter = ("organization", "type")
    list_select_related = False
    readonly_fields = ("json_data", "created", "updated")


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "updated")


@admin.register(models.Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "created", "updated", "version")
    list_filter = ("organization",)
    list_select_related = False
    readonly_fields = ("data", "created", "updated", "updated_by", "created_by")


@admin.register(models.DashboardSnapshot)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "created_by", "created", "expires")
    list_filter = (
        ("organization", admin.RelatedOnlyFieldListFilter),
        ("created_by", admin.RelatedOnlyFieldListFilter),
    )


@admin.register(models.Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "tags", "type", "_created", "_updated")
    list_filter = (
        ("organization", admin.RelatedOnlyFieldListFilter),
        ("user", admin.RelatedOnlyFieldListFilter),
    )

    def _created(self, obj):
        return datetime.datetime.fromtimestamp(obj.created / 1000)

    def _updated(self, obj):
        return datetime.datetime.fromtimestamp(obj.updated / 1000)
