from django.contrib import admin
from .models import Taskboard, EstimateHistory

admin.site.register(Taskboard)
admin.site.register(EstimateHistory)