from rest_framework.routers import DefaultRouter

from manager.views import TaskboardViewSet

router = DefaultRouter()
router.register(r'taskboard', TaskboardViewSet, basename='taskboard')