from rest_framework.routers import DefaultRouter

from manager.views import TaskboardViewSet, EventViewSet, TaskViewSet, EstimateHistoryViewset, VelocityViewSet

router = DefaultRouter()
router.register(r'taskboards', TaskboardViewSet, basename='taskboards')
router.register(r'events', EventViewSet, basename='events')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'estimate_history', EstimateHistoryViewset, basename='estimate_histories')
router.register(r'velocity', VelocityViewSet, basename='velocity')