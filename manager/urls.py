"""Module for handling url paths."""
from django.urls import path
from . import views

app_name = "manager"
urlpatterns = [
    path("taskboard/", views.TaskboardIndexView.as_view(), name="taskboard_index"),
    path("taskboard/<int:pk>/", views.TaskboardView.as_view(), name="taskboard"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),

    path("taskboard/<int:taskboard_id>/burndown/", views.BurndownView.as_view(), name="burndown_chart"),
    path("taskboard/<int:taskboard_id>/burndown/data/", views.EstimateHistoryViewset.as_view(), name="est_hist_data"),

    # path("taskboard/<int:taskboard_id>/burndown/response/", views.estimate_histories_json, name="est_hist_json"),
    # path("taskboard/<int:taskboard_id>/burndown/response/<int:eh_id>", views.estimate_histories_detail, name="est_hist_detail")
]