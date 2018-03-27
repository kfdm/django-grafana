from django.db import models

# Referenced using 'inspectdb --database grafana'


class Organization(models.Model):
    name = models.CharField(unique=True, max_length=190)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'org'


class Dashboard(models.Model):
    version = models.IntegerField()
    slug = models.CharField(max_length=189)
    title = models.CharField(max_length=189)
    data = models.TextField()
    organization = models.ForeignKey(
        'grafana.Organization',
        db_column='org_id',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField()
    updated = models.DateTimeField()
    updated_by = models.ForeignKey(
        'grafana.User',
        db_column='updated_by',
        on_delete=models.CASCADE,
        related_name='+',
    )
    created_by = models.ForeignKey(
        'grafana.User',
        db_column='created_by',
        on_delete=models.CASCADE,
        related_name='dashboard_set',
    )
    gnet_id = models.BigIntegerField(blank=True, null=True)
    uid = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dashboard'


class DashboardTag(models.Model):
    dashboard = models.ForeignKey(
        'grafana.Dashboard',
        db_column='dashboard_id',
        on_delete=models.CASCADE,
        related_name="tag_set",
    )
    term = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'dashboard_tag'


class DashboardVersion(models.Model):
    dashboard = models.ForeignKey(
        'grafana.Dashboard',
        db_column='dashboard_id',
        on_delete=models.CASCADE,
        related_name="version_set",
    )
    version = models.IntegerField()
    created = models.DateTimeField()
    created_by = models.ForeignKey(
        'grafana.User',
        db_column='created_by',
        on_delete=models.CASCADE,
        related_name='+',
    )
    message = models.TextField()
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'dashboard_version'


class User(models.Model):
    version = models.IntegerField()
    login = models.CharField(unique=True, max_length=190)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.login

    class Meta:
        managed = False
        db_table = 'user'


class ApiKey(models.Model):
    organization = models.ForeignKey(
        'grafana.Organization',
        db_column='org_id',
        on_delete=models.CASCADE,
        related_name="apikey_set",
    )
    name = models.CharField(max_length=190)
    key = models.CharField(unique=True, max_length=190)
    role = models.CharField(max_length=255)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_key'


class DataSource(models.Model):
    organization = models.ForeignKey(
        'grafana.Organization',
        db_column='org_id',
        on_delete=models.CASCADE,
        related_name="datasource_set",
    )

    type = models.CharField(max_length=255)
    name = models.CharField(max_length=190)
    access = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    json_data = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'data_source'
        unique_together = (('organization', 'name'),)
