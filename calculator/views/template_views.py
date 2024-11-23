"""API Views for A-Level Calculator page."""

from django.http.response import HttpResponseRedirect
from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin


class ALevelView(PermissionRequiredMixin, generic.TemplateView):
    """Base class to check permission of A-level calculator related views."""

    permission_required = "manager.is_taking_A_levels"

    def handle_no_permission(self) -> HttpResponseRedirect:
        """Redirect user to profile page when user has no permission."""
        messages.error(self.request, "You don't have permission to A-level Calculator.")
        return HttpResponseRedirect(reverse("manager:profile"))


class CalculatorView(ALevelView):
    """A view that displays the calculator."""

    template_name = "calculator/calculator.html"
    permission_required = "manager.is_taking_A_levels"


class MajorView(ALevelView):
    """Displays the major selection and score weight input fields of the calculator."""

    template_name = "calculator/major.html"
    permission_required = "manager.is_taking_A_levels"


class ScoreView(ALevelView):
    """A view that displays the score of the calculation."""

    template_name = "calculator/score.html"
    permission_required = "manager.is_taking_A_levels"

    def get(self, request, *args, **kwargs):
        """Override default GET to check whether user has computed in the session."""
        if "has_score" not in request.session or not "has_score":
            return redirect(reverse("calculator:calculator"))
        return super().get(request, *args, **kwargs)
