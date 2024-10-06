"""Module for handling url paths."""
from django.urls import path
from . import views


app_name = "manager"
urlpatterns = [
    path("<int:pk>taskboard/", views.IndexView.as_view(), name="taskboard"),
]