import os

import requests
from requests.auth import AuthBase

from django.conf import settings


class GrafanaAuth(AuthBase):
    def __init__(self, org):
        self.org = org

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + os.environ["GRAFANA_TOKEN"]
        r.headers["User-agent"] = getattr(settings, "USER_AGENT", "django-grafana")
        return r


def dashboard(instance, data):
    response = requests.post(
        "{}/api/dashboards/db".format(os.environ["GRAFANA_URL"]),
        auth=GrafanaAuth(instance.organization),
        json={"dashboard": data, "overwrite": True, "message": "Updated via API"},
    )
    response.raise_for_status()
    return response
