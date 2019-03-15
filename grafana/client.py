import os

import requests
from requests.auth import AuthBase


class GrafanaAuth(AuthBase):
    def __init__(self, org):
        self.org = org

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + os.environ["GRAFANA_TOKEN"]
        return r


def dashboard(instance, data):
    response = requests.post(
        "{}/api/dashboards/db".format(os.environ["GRAFANA_URL"]),
        auth=GrafanaAuth(instance.organization),
        json={"dashboard": data, "overwrite": True, "message": "Updated via API"},
    )
    response.raise_for_status()
    return response
