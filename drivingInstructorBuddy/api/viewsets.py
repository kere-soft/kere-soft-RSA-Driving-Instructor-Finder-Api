from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import response, decorators, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserCreateSerializer, UserVerifySerializer

User = get_user_model()


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
@atomic
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    res = {
        "verification_code": user.verification_code,
        "is_verified": user.is_verified,
        "user_id": user.id,
    }
    return response.Response(res, status.HTTP_201_CREATED)


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.AllowAny])
def verify_user(request):
    serializer = UserVerifySerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.update(User.objects.get(pk=request.data['id']), serializer.validated_data)
    # user can be used to send some more information related to user. Good to send user verification status so that
    # it can be updated in redux state
    return response.Response({'updated': True}, status.HTTP_200_OK)
