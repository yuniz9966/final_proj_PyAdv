import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.utils import timezone
from applications.user.models import User

fake = Faker("de_DE")  # Немецкая локаль для реалистичных данных

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'email')  # Избегаем дубликатов

    username = factory.LazyAttribute(lambda _: fake.unique.user_name())
    email = factory.LazyAttribute(lambda _: fake.unique.email())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    role = factory.LazyAttribute(lambda _: fake.random_element(
        elements=[choice[0] for choice in User.ROLE_CHOICES]
    ))
    phone = factory.LazyAttribute(lambda _: fake.phone_number())
    is_staff = False
    is_active = True
    date_joined = factory.LazyAttribute(lambda _: timezone.now())
    birth_day = factory.LazyAttribute(lambda _: fake.date_of_birth(minimum_age=18, maximum_age=80))
    password = factory.PostGenerationMethodCall('set_password', 'password123')
