"""View for handling profile update."""

from typing import Any
from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from manager.models import ParentInfo, StudentInfo, User


class ProfileView(ListView):
    """A view for the user to view/edit thier profile."""

    template_name = "manager/profile.html"
    context_object_name = "related_users"

    def get_queryset(self) -> models.QuerySet[Any]:
        """Return a query set of children if the user is a parent and vice versa."""
        user = self.request.user
        if user.has_perm("manager.is_parent"):
            print(user.student_set.all())
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
    :return: redirect to the profile page
    """
    user = request.user
    if user.has_perm("manager.is_parent"):
        info = ParentInfo.objects.get(user=user)
    else:
        info = StudentInfo.objects.get(user=user)
    info.displayed_name = request.POST["name"]
    info.save()
    return HttpResponseRedirect(reverse("manager:profile"))

def add_parent(request):
    """Add a parent to student information.
    
    :param request: request from the user
    :return: redirect to the profile page
    """
    try:
        parent_user = User.objects.get(email=request.POST["email"])
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("manager:profile"))
    if not parent_user.has_perm("manager.is_parent"):
        return HttpResponseRedirect(reverse("manager:profile"))
    user = request.user
    info = StudentInfo.objects.get(user=user)
    info.parent.add(parent_user)
    return HttpResponseRedirect(reverse("manager:profile"))

def remove_parent(request):
    """Remove a parent from student information.
    
    :param request: request from the user
    :return: redirect to the profile page
    """
    try:
        parent_user = User.objects.get(email=request.POST["email"])
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("manager:profile"))
    user = request.user
    info = StudentInfo.objects.get(user=user)
    info.parent.remove(parent_user)
    return HttpResponseRedirect(reverse("manager:profile"))

def remove_child(request):
    """Remove a student from parent information.
    
    :param request: request from the user
    :return: redirect to the profile page
    """
    try:
        student_info = StudentInfo.objects.get(user__email=request.POST["email"])
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("manager:profile"))
    user = request.user
    user.student_set.remove(student_info)
    return HttpResponseRedirect(reverse("manager:profile"))
