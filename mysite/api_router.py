from rest_framework.routers import DefaultRouter
from manager.views import TaskboardViewSet, EventViewSet, TaskViewSet
from calculator.views import ExamsViewSet, UniversityViewSet, FacultyViewSet, MajorViewSet, CriteriaViewSet, StudentExamScoreViewSet


router = DefaultRouter()
router.register(r'taskboards', TaskboardViewSet, basename='taskboards')
router.register(r'events', EventViewSet, basename='events')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'exams', ExamsViewSet, basename='exams')
router.register(r'universities', UniversityViewSet, basename="universities")
router.register(r'faculties', FacultyViewSet, basename="faculties")
router.register(r'majors', MajorViewSet, basename="majors")
router.register(r'criteria', CriteriaViewSet, basename="criteria")
router.register(r'exam_score', StudentExamScoreViewSet, basename="exam_score")
