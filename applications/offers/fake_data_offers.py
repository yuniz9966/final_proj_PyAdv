import factory
from factory.django import DjangoModelFactory
from faker import Faker
import random

from applications.offers.models import Offer
from applications.extra.models import Location
from applications.offers.choices.room_type import RoomType
from applications.user.fake_data_user import UserFactory

fake = Faker("de_DE")  # Немецкая локаль

class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location
        django_get_or_create = ('city', 'district', 'street', 'postal_code')

    city = factory.Faker('city', locale='de_DE')
    district = factory.LazyAttribute(lambda _: fake.city_suffix() or "")
    street = factory.Faker('street_address', locale='de_DE')
    postal_code = factory.Faker('postcode', locale='de_DE')
    country = "Germany"
    latitude = factory.LazyAttribute(lambda _: random.uniform(47.0, 55.0))
    longitude = factory.LazyAttribute(lambda _: random.uniform(5.0, 15.0))

class RentHouseFactory(DjangoModelFactory):
    class Meta:
        model = Offer

    title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=4))
    description = factory.LazyAttribute(lambda _: fake.paragraph(nb_sentences=3))
    location = factory.SubFactory(LocationFactory)
    price = factory.LazyAttribute(lambda _: round(
        fake.pydecimal(
            left_digits=4,
            right_digits=2,
            positive=True
        ), 2
    ))
    room_type = factory.LazyAttribute(lambda _: fake.random_element(
        RoomType.faker_choices()
    ))
    rooms_count = factory.LazyAttribute(
        lambda o: 1 if o.room_type == RoomType.STUDIO else fake.random_int(min=1, max=6)
    )
    is_active = True
    owner = factory.SubFactory(UserFactory)


# import factory
# from faker import Faker
# from applications.offers.models import Offer
# from applications.user.fake_data_user import UserFactory
#
# fake = Faker("de_DE")
#
# class RentHouseFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Offer
#
#     title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=4))
#     owner = factory.SubFactory(UserFactory, role='OWNER')
#     # Другие поля (например, location)
#
#     @classmethod
#     def _create(cls, model_class, *args, **kwargs):
#         # Если owner не передан, используем существующий
#         if 'owner' not in kwargs:
#             from applications.user.models import User
#             owners = User.objects.filter(role='OWNER')
#             kwargs['owner'] = fake.random_element(owners) if owners.exists() else UserFactory(role='OWNER')
#         return super()._create(model_class, *args, **kwargs)