"""API Views for A-Level Calculator page."""

from django.views import generic


class CalculatorView(generic.TemplateView):
    """A view that displays the calculator."""

    template_name = "calculator/calculator.html"


class MajorView(generic.TemplateView):
    """Displays the major selection and score weight input fields of the calculator."""

    template_name = "calculator/major.html"


class ScoreView(generic.TemplateView):
    """A view that displays the score of the calculation."""

    template_name = "calculator/score.html"
