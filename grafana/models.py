from django.db import models

# Referenced using 'inspectdb --database grafana'


class Organization(models.Model):
    name = models.CharField(unique=True, max_length=190)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'org'


class Dashboard(models.Model):
    version = models.IntegerField()
    slug = models.CharField(max_length=189)
    title = models.CharField(max_length=189)
    data = models.TextField()
    orginization = models.ForeignKey(
        'grafana.Organization',
        db_column='org_id',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField()
    updated = models.DateTimeField()
    updated_by = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    gnet_id = models.BigIntegerField(blank=True, null=True)
    plugin_id = models.CharField(max_length=255, blank=True, null=True)
    folder_id = models.BigIntegerField()
    is_folder = models.BooleanField()
    has_acl = models.BooleanField()
    uid = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dashboard'
