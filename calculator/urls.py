from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = "calculator"
urlpatterns = [
    path('api/', views.CalculatorAPIView.as_view(), name='calc_api'),
    path('/', views.CalculatorView.as_view(), name='calculator')
]

# wtf is this?
# urlpatterns = format_suffix_patterns(urlpatterns)
