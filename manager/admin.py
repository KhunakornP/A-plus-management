from django.contrib import admin
from .models import Taskboard, EstimateHistory, Event, Task, StudentInfo

admin.site.register(Taskboard)
admin.site.register(Event)
admin.site.register(Task)
admin.site.register(EstimateHistory)
admin.site.register(StudentInfo)