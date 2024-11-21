"""API Views for A-Level Calculator page."""

from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse


class CalculatorView(generic.TemplateView):
    """A view that displays the calculator."""

    template_name = "calculator/calculator.html"


class MajorView(generic.TemplateView):
    """Displays the major selection and score weight input fields of the calculator."""

    template_name = "calculator/major.html"


class ScoreView(generic.TemplateView):
    """A view that displays the score of the calculation."""

    template_name = "calculator/score.html"

    def get(self, request, *args, **kwargs):
        """Override default GET to check whether user has computed in the session."""
        if "has_score" not in request.session or not "has_score":
            return redirect(reverse("calculator:calculator"))
        return super().get(request, *args, **kwargs)
