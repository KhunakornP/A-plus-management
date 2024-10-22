from rest_framework.routers import DefaultRouter

from manager.views import TaskboardViewSet, EventViewSet

router = DefaultRouter()
router.register(r'taskboard', TaskboardViewSet, basename='taskboard')
router.register(r'event', EventViewSet, basename='event')