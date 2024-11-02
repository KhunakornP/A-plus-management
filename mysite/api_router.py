from rest_framework.routers import DefaultRouter
from manager.views import TaskboardViewSet, EventViewSet, TaskViewSet
from calculator.views import ExamsViewSet


router = DefaultRouter()
router.register(r'taskboards', TaskboardViewSet, basename='taskboards')
router.register(r'events', EventViewSet, basename='events')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'exams', ExamsViewSet, basename='exams')
