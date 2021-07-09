from grafana import views

from django.urls import path

app_name = "grafana"
urlpatterns = [
    path("", views.OrganizationListView.as_view(), name="org-list"),
    path("org/<int:pk>", views.OrganizationDetailView.as_view(), name="org-detail"),
    path("org/<int:pk>/annotations", views.AnnotationList.as_view(), name="org-annotations"),
    path("org/<int:pk>/versions", views.VersionList.as_view(), name="org-versions"),
    path("org/<int:pk>/users", views.UserList.as_view(), name="org-users"),
    path("dash/<int:pk>/mutate", views.DashboardMutate.as_view(), name="dash-mutate"),
    path("dash/<int:pk>", views.DashboardDetailView.as_view(), name="dash-detail"),
    path("version/<int:pk>", views.RevisionVersion.as_view(), name="version-detail"),
]
