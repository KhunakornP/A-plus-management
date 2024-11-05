"""Views for the parent dashboard."""

from django.shortcuts import redirect, reverse
from django.views import generic


class DashboardView(generic.ListView):
    """View that displays the parent dashboard."""

    template_name = "manager/dashboard.html"
    context_object_name = "child_list"

    def get_queryset(self):
        """Returns all children associated with the user."""
        return self.request.user.student_set.all()

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
