"""View for handling profile update."""

from typing import Any
from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.models import Permission
from manager.models import ParentInfo, StudentInfo, User


class ProfileView(ListView):
    """A view for the user to view/edit thier profile."""

    template_name = "manager/profile.html"
    context_object_name = "related_users"

    def get_queryset(self) -> models.QuerySet[Any]:
        """Return a query set of children if the user is a parent and vice versa."""
        user = self.request.user
        if user.has_perm("manager.is_parent"):
            return user.student_set.all()
        else:
            student_info = StudentInfo.objects.get(user=self.request.user)
            return student_info.parent.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add user's displayed name to context."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.has_perm("manager.is_parent"):
            info = ParentInfo.objects.get(user=user)
        else:
            info = StudentInfo.objects.get(user=user)
        context["displayed_name"] = info.displayed_name
        return context


def update_displayed_name(request):
    """Update user's displayed name.

    :param request: request from the user
    :return: a redirect response to the profile page
    """
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manager:profile"))
    user = request.user
    if user.has_perm("manager.is_parent"):
        info = ParentInfo.objects.get(user=user)
    else:
        info = StudentInfo.objects.get(user=user)
    info.displayed_name = request.POST["name"]
    info.save()
    messages.success(request, "Your displayed name has been updated.")
    return HttpResponseRedirect(reverse("manager:profile"))


def add_parent(request):
    """Add a parent to student information.

    :param request: request from the user
    :return: a redirect response to the profile page
    """
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manager:profile"))
    email = request.POST["email"]
    user = request.user
    info = StudentInfo.objects.get(user=user)
    try:
        parent_user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, f"There is no user with email: {email}.")
        return HttpResponseRedirect(reverse("manager:profile"))
    if not parent_user.has_perm("manager.is_parent"):
        messages.error(request, f"User with email: {email} is not a parent.")
        return HttpResponseRedirect(reverse("manager:profile"))
    if info.parent.filter(email=email).exists():
        messages.warning(request, f"{email} is already in the list")
        return HttpResponseRedirect(reverse("manager:profile"))
    info.parent.add(parent_user)
    messages.success(request, f"Successfully added {email} to the list.")
    return HttpResponseRedirect(reverse("manager:profile"))


def remove_parent(request):
    """Remove a parent from student information.

    :param request: request from the user
    :return: a redirect response to the profile page
    """
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manager:profile"))
    email = request.POST["email"]
    try:
        parent_user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, f"There is no user with email: {email}.")
        return HttpResponseRedirect(reverse("manager:profile"))
    user = request.user
    info = StudentInfo.objects.get(user=user)
    info.parent.remove(parent_user)
    messages.success(request, f"Successfully removed {email} from the list.")
    return HttpResponseRedirect(reverse("manager:profile"))


def remove_child(request):
    """Remove a student from parent information.

    :param request: request from the user
    :return: a redirect response to the profile page
    """
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manager:profile"))
    email = request.POST["email"]
    try:
        student_info = StudentInfo.objects.get(user__email=email)
    except StudentInfo.DoesNotExist:
        messages.error(request, f"There is no user with email: {email}.")
        return HttpResponseRedirect(reverse("manager:profile"))
    user = request.user
    user.student_set.remove(student_info)
    messages.success(request, f"Successfully removed {email} from the list.")
    return HttpResponseRedirect(reverse("manager:profile"))


def update_a_level_permission(request):
    """Update a student's permission about A-level.

    :param request: request from the user
    :return: a redirect response to the profile page
    """
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manager:profile"))
    user = request.user
    if request.POST["choice"] == "Yes":
        user.user_permissions.add(Permission.objects.get(codename="is_taking_A_levels"))
        messages.success(request, "You can now access A-level calculator.")
    if request.POST["choice"] == "No":
        user.user_permissions.remove(
            Permission.objects.get(codename="is_taking_A_levels")
        )
        messages.success(request, "Access to A-level calculator has been removed.")
    return HttpResponseRedirect(reverse("manager:profile"))
