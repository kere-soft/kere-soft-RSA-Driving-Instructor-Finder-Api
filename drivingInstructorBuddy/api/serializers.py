import random
from django.contrib.auth import get_user_model
from rest_framework import serializers
from drivingInstructorBuddy.models import Profile, Learner, Instructor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from model_utils import Choices

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = "__all__"


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    learner = LearnerSerializer()
    instructor = InstructorSerializer()

    class Meta:
        model = User
        exclude = ['password', 'verification_code', 'is_superuser', 'is_active']


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, required=True, style={
        "input_type": "email"})
    password = serializers.CharField(write_only=True, required=True, style={
        "input_type": "password"}, max_length=128)
    name = serializers.CharField(max_length=128, required=True)
    avatar = serializers.CharField(max_length=256, required=False, allow_blank=True)
    city = serializers.CharField(max_length=128, required=False, allow_blank=True)
    county = serializers.CharField(max_length=128, required=False, allow_blank=True)
    user_type = serializers.ChoiceField(choices=Choices(
        ('LEARNER', 'LEARNER'),
        ('INSTRUCTOR', 'INSTRUCTOR'),
    ))

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "name",
            "avatar",
            "city",
            "county",
            "user_type"
        ]

    def create(self, validated_data):
        print(validated_data)
        email = validated_data["email"]
        password = validated_data["password"]
        name = validated_data["name"]
        city = validated_data['city'] if 'city' in validated_data else ""
        county = validated_data['county'] if 'county' in validated_data else ""
        user_type = validated_data['user_type'] if 'user_type' in validated_data else ""
        avatar = validated_data['avatar'] if 'avatar' in validated_data else random.choice([
            'https://i.ya-webdesign.com/images/male-avatar-icon-png-7.png',
            'https://cdn1.iconfinder.com/data/icons/user-pictures/100/female1-512.png',
            'https://cdn4.iconfinder.com/data/icons/avatar-circle-1-1/72/39-512.png',
            'https://i.ya-webdesign.com/images/avatar-icon-png-1.png',
            'https://cdn2.iconfinder.com/data/icons/circle-avatars-1/128/050_girl_avatar_profile_woman_suit_student_officer-512.png',
            'https://i.ya-webdesign.com/images/male-avatar-icon-png-7.png',
        ])

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})

        user = User.objects.create_user(email=email)
        user.set_password(password)
        user.verification_code = random.randint(1111, 9999)
        if user:
            print('We are here')
            try:
                user.profile = Profile.objects.create(user=user, name=name, city=city, avatar=avatar, county=county)
                print(user.profile)
                # user.profile = profile.save()
                if user_type == "LEARNER":
                    learner = Learner.objects.create(user=user)
                    print(learner)
                    # user.learner = learner.save()
                elif user_type == "INSTRUCTOR":
                    instructor = Instructor.objects.create(user=user)
                    print(instructor)
                    # user.instructor = instructor.save()
            except Exception as e:
                raise
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
        data['id'] = self.user.id
        data['profile'] = UserProfileSerializer(self.user.profile).data
        return data
