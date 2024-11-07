"""Views for the parent dashboard."""

from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.utils import timezone
from django.views import generic
from manager.models import Task


class DashboardView(generic.ListView):
    """View that displays the parent dashboard."""

    template_name = "manager/dashboard.html"
    context_object_name = "child_list"

    def get_queryset(self):
        """Returns all children associated with the user."""
        return self.request.user.student_set.all()

    def get_context_data(self, **kwargs):
        """Pass more task data for all related students."""
        students = self.request.user.student_set.all()
        context = super().get_context_data(**kwargs)
        if students:
            today = []
            late = []
            fin = []
            for student in students:
                today.append(
                    Task.objects.filter(
                        taskboard__user=student.user, end_date__day=timezone.now().day
                    ).count()
                )
                late.append(
                    Task.objects.filter(
                        ~Q(status="DONE"),
                        taskboard__user=student.user,
                        end_date__lte=timezone.now(),
                    ).count()
                )
                fin.append(
                    Task.objects.filter(
                        taskboard__user=student.user, status="DONE"
                    ).count()
                )
            context["today"] = today
            context["late"] = late
            context["fin"] = fin
        return context

    def get(self, request, *args, **kwargs):
        """
        Override the GET request and check if the user is a parent.

        Redirect the user to the main page if they are not a parent.
        """
        # check if user is logged in
        if not self.request.user.is_authenticated:
            return redirect(reverse("manager:main_login"))
        # check if user is a parent
        if not self.request.user.has_perm("manager.is_parent"):
            return redirect(reverse("manager:taskboard_index"))
        return super().get(request, *args, **kwargs)
