from django.urls import path

from backend.apps.dashboard.api import controller as dashboard_api_views

dashboard_prefix = "api/<int:version>/dashboard/"

dashboard_paths = [
    path(
        dashboard_prefix + "health",
        dashboard_api_views.ServiceCheckAPI.as_view(),
        name="dashboard.service_check_api",
    ),
    path(
        dashboard_prefix + "users",
        dashboard_api_views.UserCreateAPIView.as_view(),
        name="dashboard.create_parent_api",
    ),
    path(
        dashboard_prefix + "users/<int:user_id>",
        dashboard_api_views.UserUpdateAPIView.as_view(),
        name="dashboard.update_parent_api",
    ),
    path(
        dashboard_prefix + "users/<int:user_id>/children/",
        dashboard_api_views.ChildrenCreateUpdateAPIView.as_view(),
        name="dashboard.update_parent_api",
    ),
    path(
        dashboard_prefix + "content-recommendation",
        dashboard_api_views.UserContentAPIView.as_view(),
        name="dashboard.content_rec_api"
    )
]