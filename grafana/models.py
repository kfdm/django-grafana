import warnings

from django.conf import settings
from django.db import models
from django.urls import reverse

# Referenced using 'inspectdb --database grafana'


class Organization(models.Model):
    name = models.CharField(unique=True, max_length=190)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "org"

    def get_absolute_url(self):
        return reverse("grafana:org-detail", args=(self.pk,))


class Dashboard(models.Model):
    version = models.IntegerField()
    slug = models.CharField(max_length=189)
    title = models.CharField(max_length=189)
    data = models.JSONField()
    organization = models.ForeignKey(
        "grafana.Organization",
        db_column="org_id",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField()
    updated = models.DateTimeField()
    updated_by = models.ForeignKey(
        "grafana.User",
        db_column="updated_by",
        on_delete=models.CASCADE,
        related_name="+",
    )
    created_by = models.ForeignKey(
        "grafana.User",
        db_column="created_by",
        on_delete=models.CASCADE,
        related_name="dashboard_set",
    )
    gnet_id = models.BigIntegerField(blank=True, null=True)
    uid = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "dashboard"

    def json(self):
        warnings.warn("Switch to native JSONField", DeprecationWarning, stacklevel=1)
        return self.data

    def get_public_link(self):
        return "{base}/d/{d.uid}?orgId={d.organization_id}".format(
            base=settings.GRAFANA_URL,
            d=self,
        )

    def get_absolute_url(self):
        return reverse("grafana:dash-detail", args=(self.pk,))


class DashboardTag(models.Model):
    dashboard = models.ForeignKey(
        "grafana.Dashboard",
        db_column="dashboard_id",
        on_delete=models.CASCADE,
        related_name="tag_set",
    )
    term = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "dashboard_tag"


class DashboardVersion(models.Model):
    dashboard = models.ForeignKey(
        "grafana.Dashboard",
        db_column="dashboard_id",
        on_delete=models.CASCADE,
        related_name="version_set",
    )
    version = models.IntegerField()
    created = models.DateTimeField()
    created_by = models.ForeignKey(
        "grafana.User",
        db_column="created_by",
        on_delete=models.CASCADE,
        related_name="+",
    )
    message = models.TextField()
    data = models.JSONField()

    class Meta:
        managed = False
        db_table = "dashboard_version"

    def json(self):
        warnings.warn("Switch to native JSONField", DeprecationWarning, stacklevel=1)
        return self.data

    def get_absolute_url(self):
        return reverse("grafana:version-detail", args=(self.pk,))


class User(models.Model):
    version = models.IntegerField()
    login = models.CharField(unique=True, max_length=190)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=190, blank=True, null=True)

    created = models.DateTimeField()
    updated = models.DateTimeField()
    last_seen_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.login

    class Meta:
        managed = False
        db_table = "user"


class ApiKey(models.Model):
    organization = models.ForeignKey(
        "grafana.Organization",
        db_column="org_id",
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
        db_table = "api_key"


class DataSource(models.Model):
    organization = models.ForeignKey(
        "grafana.Organization",
        db_column="org_id",
        on_delete=models.CASCADE,
        related_name="datasource_set",
    )

    type = models.CharField(max_length=255)
    name = models.CharField(max_length=190)
    access = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    json_data = models.JSONField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "data_source"
        unique_together = (("organization", "name"),)


class DashboardSnapshot(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    key = models.CharField(unique=True, max_length=190)
    delete_key = models.CharField(unique=True, max_length=190)
    organization = models.ForeignKey(
        "grafana.Organization",
        db_column="org_id",
        on_delete=models.CASCADE,
        related_name="snapshot_set",
    )
    created_by = models.ForeignKey(
        "grafana.User",
        db_column="user_id",
        on_delete=models.CASCADE,
        related_name="snapshot_set",
    )
    external = models.IntegerField()
    external_url = models.CharField(max_length=255)
    dashboard = models.TextField()
    expires = models.DateTimeField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "dashboard_snapshot"


class Annotation(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField()
    text = models.TextField()
    tags = models.CharField(max_length=500)
    type = models.CharField(max_length=25)

    created = models.IntegerField()
    updated = models.IntegerField()

    alert_id = models.IntegerField()
    epoch = models.IntegerField()
    epoch_end = models.IntegerField()

    organization = models.ForeignKey(
        "grafana.Organization",
        db_column="org_id",
        on_delete=models.CASCADE,
        related_name="annotation_set",
    )

    user = models.ForeignKey(
        "grafana.User",
        db_column="user_id",
        on_delete=models.CASCADE,
        related_name="annotation_set",
    )

    class Meta:
        managed = False
        db_table = "annotation"


class Invite(models.Model):
    organization = models.ForeignKey(
        "grafana.Organization",
        db_column="org_id",
        on_delete=models.CASCADE,
        related_name="invite_set",
    )
    version = models.IntegerField()
    email = models.CharField(max_length=190)
    name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, blank=True, null=True)
    code = models.CharField(max_length=190)
    status = models.CharField(max_length=20)
    invited_by = models.ForeignKey(
        "grafana.User",
        db_column="invited_by_user_id",
        on_delete=models.CASCADE,
        related_name="+",
    )
    email_sent = models.IntegerField()
    email_sent_on = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "temp_user"


class Team(models.Model):
    name = models.CharField(max_length=190)
    organization = models.ForeignKey(
        "grafana.Organization",
        db_column="org_id",
        on_delete=models.CASCADE,
        related_name="team_set",
    )
    created = models.DateTimeField()
    updated = models.DateTimeField()
    email = models.CharField(max_length=190, blank=True, null=True)
    members = models.ManyToManyField(User, through="TeamMember")

    class Meta:
        managed = False
        db_table = "team"
        unique_together = (("organization", "name"),)


class TeamMember(models.Model):
    organization = models.ForeignKey(
        "grafana.Organization",
        db_column="org_id",
        on_delete=models.CASCADE,
        related_name="+",
    )
    team = models.ForeignKey(
        "grafana.Team", db_column="team_id", on_delete=models.CASCADE, related_name="+"
    )
    user = models.ForeignKey(
        "grafana.User", db_column="user_id", on_delete=models.CASCADE, related_name="+"
    )
    created = models.DateTimeField()
    updated = models.DateTimeField()
    external = models.IntegerField(blank=True, null=True)
    permission = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "team_member"
        unique_together = (("organization", "team", "user"),)


class OrgMember(models.Model):
    organization = models.ForeignKey(
        "grafana.Organization",
        db_column="org_id",
        on_delete=models.CASCADE,
        related_name="+",
    )
    user = models.ForeignKey(
        "grafana.User",
        db_column="user_id",
        on_delete=models.CASCADE,
        related_name="+",
    )
    created = models.DateTimeField()
    updated = models.DateTimeField()
    role = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = "org_user"
