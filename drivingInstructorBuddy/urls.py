from django.urls import path
from rest_framework.routers import SimpleRouter
from .viewsets import NoteViewSet

router = SimpleRouter()
router.register('drivingInstructorBuddy', NoteViewSet, basename="notes")
urlpatterns = router.urls
