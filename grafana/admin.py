from django.contrib import admin
from grafana import models


@admin.register(models.DataSource)
class DatasourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'type')
    list_filter = ('organization', 'type')
    list_select_related = False
    readonly_fields = ('json_data', 'created', 'updated')


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')


@admin.register(models.Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'created', 'updated', 'version')
    list_filter = ('organization',)
    list_select_related = False
    readonly_fields = ('data', 'created', 'updated', 'updated_by', 'created_by')
