"""Module for handling url paths."""
from django.urls import path
from . import views


app_name = "manager"
urlpatterns = [
    path("taskboard/", views.TaskboardIndexView.as_view(), name="taskboard_index"),
    path("taskboard/<int:taskboard_id>/delete/", views.delete_taskboard, name="delete_taskboard"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path("taskboard/<int:pk>/", views.TaskboardView.as_view(), name="taskboard"),
    path("taskboard/<int:taskboard_id>/add_task/", views.create_task, name="create_task"),
    path("task/<int:task_id>/delete/", views.delete_task, name="delete_task")
]