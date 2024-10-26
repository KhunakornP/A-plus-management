from django.contrib import admin
from .models import Taskboard, EstimateHistory, Task

admin.site.register(Taskboard)
admin.site.register(Task)
admin.site.register(EstimateHistory)