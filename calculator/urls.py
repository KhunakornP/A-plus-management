from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('api/', views.CalculatorAPIView.as_view(), name='calc_api'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
