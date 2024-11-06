"""Module for handling url paths."""
from django.urls import path
from . import views

app_name = "manager"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="main_login"),
    path("setup/", views.UserSetupView.as_view(), name="user_setup"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("taskboard/", views.TaskboardIndexView.as_view(), name="taskboard_index"),
    path("taskboard/<int:pk>/", views.TaskboardView.as_view(), name="taskboard"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path("taskboard/<int:taskboard_id>/burndown/", views.BurndownView.as_view(), name="burndown_chart"),
    path("taskboard/<int:taskboard_id>/burndown/response/", views.estimate_histories_json, name="est_hist_json"),
    path("taskboard/index/<int:user_id>/", views.get_user_taskboard, name="user_tb_index")
]