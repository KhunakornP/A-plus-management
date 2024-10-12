"""Module for handling url paths."""
from django.urls import path
from . import views


app_name = "manager"
urlpatterns = [
    path("taskboard/", views.TaskboardView.as_view(), name="taskboard"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path("event/create/", views.create_event, name="create_event"),
    path("event/<int:event_id>/delete/", views.delete_event, name="delete_event"),
    path("event/<int:event_id>/update/", views.update_event, name="update_event"),
]