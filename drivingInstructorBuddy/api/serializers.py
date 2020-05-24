import random
from django.contrib.auth import get_user_model
from rest_framework import serializers
from drivingInstructorBuddy.models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = User
        exclude = ['password', 'verification_code', 'is_superuser', 'is_active']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
        "input_type": "password"}, max_length=128)
    email = serializers.CharField(write_only=True, required=True, style={
        "input_type": "email"})
    name = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = [
            "email",
            "verification_code",
            "is_verified",
            "password",
            "name"
        ]

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        name = validated_data["name"]
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})

        user = User.objects.create_user(email=email,name=name)
        user.set_password(password)
        user.verification_code = random.randint(1111, 9999)
        user.save()
        return user


class UserVerifySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    verification_code = serializers.IntegerField(required=True)
    class Meta:
        model = User
        fields = [
            "id",
            "verification_code"
        ]

    def update(self, instance, validated_data):
        print(validated_data)
        if instance.verification_code != validated_data['verification_code']:
            raise serializers.ValidationError(
                {"verification": "Incorrect verification code!"})
        instance.is_verified = True
        instance.save()
        return instance


class CustomTokenTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_verified'] = self.user.is_verified
        data['id']=self.user.id
        return data



