from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drivingInstructorBuddy.api.viewsets import registration, verify_user, CustomTokenObtainPairView

router = SimpleRouter()
# router.register('drivingInstructorBuddy', NoteViewSet, basename="notes")

urlpatterns = [
    path("register/", registration, name='register'),
    path("verify/", verify_user, name='verify_user'),
    path("token/", CustomTokenObtainPairView.as_view(), name="custom_token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

