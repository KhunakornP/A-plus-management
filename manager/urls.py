"""Module for handling url paths."""
from django.urls import path
from . import views





app_name = "manager"
urlpatterns = [
    path("taskboard/", views.TaskboardIndexView.as_view(), name="taskboard_index"),
    path("taskboard/<int:pk>/", views.TaskboardView.as_view(), name="taskboard"),
    path("taskboard/create/", views.create_taskboard, name="create_taskboard"),
    path("taskboard/<int:taskboard_id>/delete/", views.delete_taskboard, name="delete_taskboard"),
    path("taskboard/<int:taskboard_id>/update/", views.update_taskboard, name="update_taskboard"),
    path("taskboard/<int:taskboard_id>/add_task/", views.create_task, name="create_task"),
    path("task/<int:task_id>/delete/", views.delete_task, name="delete_task"),
    path("task/<int:task_id>/update/", views.update_task, name="update_task"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path("event/create/", views.create_event, name="create_event"),
    path("event/<int:event_id>/delete/", views.delete_event, name="delete_event"),
    path("event/<int:event_id>/update/", views.update_event, name="update_event"),
    path("taskboard/<int:taskboard_id>/burndown/", views.BurndownView.as_view(), name="burndown_chart"),
    path("taskboard/<int:taskboard_id>/burndown/response/", views.estimate_histories_json, name="est_hist_json")
]