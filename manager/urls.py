"""Module for handling url paths."""
from django.urls import path
from . import views


app_name = "manager"
urlpatterns = [
    path("taskboard/", views.TaskboardIndexView.as_view(), name="taskboard_index"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path("taskboard/<int:pk>", views.TaskboardView.as_view(), name="taskboard"),
]