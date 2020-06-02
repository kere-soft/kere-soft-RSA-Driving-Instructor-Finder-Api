import random
from factory import DjangoModelFactory, lazy_attribute, RelatedFactory
from .models import *
from faker import Faker
from faker.providers import BaseProvider


class CityProvider(BaseProvider):
    def cities(self):
        cities = ['Athlone', 'Galway', 'Dublin']
        return random.choice(cities)


class VerificationCodeProvider(BaseProvider):
    def verification_code(self):
        return random.randint(1111, 9999)


class CountyProvider(BaseProvider):
    def counties(self):
        counties = ['Westmeath', 'Kerry', 'Meath']
        return random.choice(counties)


class AvatarProvider(BaseProvider):
    def avatar(self):
        avatars = [
            'https://i.ya-webdesign.com/images/male-avatar-icon-png-7.png',
            'https://cdn1.iconfinder.com/data/icons/user-pictures/100/female1-512.png',
            'https://cdn4.iconfinder.com/data/icons/avatar-circle-1-1/72/39-512.png',
            'https://i.ya-webdesign.com/images/avatar-icon-png-1.png',
            'https://cdn2.iconfinder.com/data/icons/circle-avatars-1/128'
            '/050_girl_avatar_profile_woman_suit_student_officer-512.png',
            'https://i.ya-webdesign.com/images/male-avatar-icon-png-7.png',
        ]
        return random.choice(avatars)


faker = Faker()
faker.add_provider(CityProvider)
faker.add_provider(CountyProvider)
faker.add_provider(AvatarProvider)
faker.add_provider(VerificationCodeProvider)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = lazy_attribute(lambda x: faker.email())
    password = lazy_attribute(lambda x: faker.password())
    verification_code = lazy_attribute(lambda x: faker.verification_code())
    is_verified = False
    is_active = True
    is_superuser = False


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = RelatedFactory(UserFactory)
    name = lazy_attribute(lambda x: faker.name())
    avatar = lazy_attribute(lambda x: faker.avatar())
    city = lazy_attribute(lambda x: faker.cities())
    county = lazy_attribute(lambda x: faker.counties())


class LearnerFactory(DjangoModelFactory):
    class Meta:
        model = Learner

    user = RelatedFactory(UserFactory)


class InstructorFactory(DjangoModelFactory):
    class Meta:
        model = Instructor

    user = RelatedFactory(UserFactory)
    recommendations = lazy_attribute(lambda x: random.randint(0, 50))
    about = lazy_attribute(lambda x: faker.text())
