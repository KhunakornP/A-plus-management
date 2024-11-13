from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = "calculator"
urlpatterns = [
    path('', views.CalculatorView.as_view(), name='calculator'),
    path('1', views.CalculatorView.as_view(), name='calculator_alt'),
    path('2', views.MajorView.as_view(), name='major'),
    path('3', views.ScoreView.as_view(), name='score'),
]

# wtf is this?
# urlpatterns = format_suffix_patterns(urlpatterns)
