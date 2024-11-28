from django.contrib import admin
from .models import Taskboard, EstimateHistory, Event, Task, StudentInfo, ParentInfo
from calculator.models import University, Faculty, Major, CriteriaSet, Exams, Criterion, StudentExamScore


admin.site.register(Taskboard)
admin.site.register(Event)
admin.site.register(Task)
admin.site.register(EstimateHistory)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Major)
admin.site.register(CriteriaSet)
admin.site.register(Criterion)
admin.site.register(Exams)
admin.site.register(StudentExamScore)
admin.site.register(StudentInfo)
admin.site.register(ParentInfo)
