from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import response, decorators, permissions, status
from .serializers import UserSerializer, RegistrationSerializer, UserVerifySerializer, \
    CustomTokenTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenTokenObtainPairSerializer


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
@atomic
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    user_data = UserSerializer(user).data
    return response.Response(user_data, status.HTTP_201_CREATED)


@decorators.api_view(["PUT"])
@decorators.permission_classes([permissions.AllowAny])
def verify_user(request):
    serializer = UserVerifySerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.update(User.objects.get(pk=request.data['id']), serializer.validated_data)
    user_data = UserSerializer(user).data
    return response.Response(user_data, status.HTTP_200_OK)
