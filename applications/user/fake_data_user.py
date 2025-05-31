import factory
from faker import Faker
from applications.user.models import User

fake = Faker("de_DE")

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(lambda _: fake.unique.user_name())
    email = factory.LazyAttribute(lambda _: fake.unique.email())
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    role = factory.Iterator(['RENTER', 'OWNER'])
