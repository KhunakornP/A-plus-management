"""Module for handling url paths."""
from django.urls import path
from . import views


app_name = "manager"
urlpatterns = [
    path("taskboard/", views.TaskboardView.as_view(), name="taskboard"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
]