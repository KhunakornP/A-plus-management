"""Module for handling url paths."""
from django.urls import path
from . import views

app_name = "manager"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="main_login"),
    path("setup/", views.UserSetupView.as_view(), name="user_setup"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/update_name", views.update_displayed_name, name="update_displayed_name"),
    path("profile/add_parent", views.add_parent, name="add_parent"),
    path("profile/remove_parent", views.remove_parent, name="remove_parent"),
    path("profile/remove_child", views.remove_child, name="remove_child"),
    path("profile/update_a_level", views.update_a_level_permission, name="update_a_level"),
    path("taskboard/", views.TaskboardIndexView.as_view(), name="taskboard_index"),
    path("taskboard/<int:pk>/", views.TaskboardView.as_view(), name="taskboard"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path("taskboard/<int:taskboard_id>/burndown/", views.BurndownView.as_view(), name="burndown_chart"),
    path("taskboard/<int:taskboard_id>/burndown/response/", views.estimate_histories_json, name="est_hist_json"),
    path("taskboard/index/<int:user_id>/", views.get_user_taskboard, name="user_tb_index"),
    path("taskboard/<int:user_id>/<int:taskboard_id>/", views.get_taskboard_details, name="user_tb_details"),
    path("chart/index/<int:user_id>/", views.ChartIndexView.as_view(), name="chart_index")
]