from django.contrib import admin
from .models import Taskboard, EstimateHistory, Task, Event

admin.site.register(Taskboard)
admin.site.register(Task)
admin.site.register(EstimateHistory)
admin.site.register(Event)