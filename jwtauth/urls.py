from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import registration, protected_route

urlpatterns = [
    path('register/', registration, name='register'),
    path('protected_route/', protected_route, name='protected_route'),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
