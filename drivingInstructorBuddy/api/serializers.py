import random
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
        "input_type": "password"})
    email = serializers.CharField(write_only=True, required=True, style={
        "input_type": "email"})

    class Meta:
        model = User
        fields = [
            "email",
            "verification_code",
            "is_verified",
            "password",
        ]

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})

        user = User(email=email)
        user.set_password(password)
        user.verification_code = random.randint(1111, 9999)
        user.save()
        return user


class UserVerifySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    verification_code = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ["id", "verification_code"]

    def update(self, instance, validated_data):

        print(validated_data['verification_code'])
        print(validated_data)
        if instance.verification_code != validated_data['verification_code']:
            raise serializers.ValidationError(
                {"verification": "Incorrect verification code!"})
        instance.is_verified = True
        instance.save()

