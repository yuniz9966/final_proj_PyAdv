import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.utils import timezone
from applications.bookings.models import Booking, BookingStatus
from applications.offers.fake_data_offers import RentHouseFactory
from applications.user.fake_data_user import UserFactory

fake = Faker("de_DE")

class BookingFactory(DjangoModelFactory):
    class Meta:
        model = Booking

    offer = factory.SubFactory(RentHouseFactory)
    renter = factory.SubFactory(UserFactory, role='RENTER')
    start_date = factory.LazyAttribute(lambda _: fake.date_time_between(start_date='now', end_date='+30d'))
    end_date = factory.LazyAttribute(lambda o: o.start_date + timezone.timedelta(days=fake.random_int(min=5, max=30)))
    status = factory.LazyAttribute(lambda _: fake.random_element(elements=[choice[0] for choice in BookingStatus.choices]))
    created_at = factory.LazyAttribute(lambda _: timezone.now())
    updated_at = factory.LazyAttribute(lambda _: timezone.now())
