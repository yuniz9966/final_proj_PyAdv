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


# import factory
# from faker import Faker
# from django.utils import timezone
# from applications.bookings.models import Booking, BookingStatus
# from applications.user.fake_data_user import UserFactory
# from applications.offers.fake_data_offers import RentHouseFactory
#
# fake = Faker("de_DE")
#
# class BookingFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Booking
#
#     renter = factory.SubFactory(UserFactory, role='RENTER')
#     offer = factory.SubFactory(RentHouseFactory)
#     start_date = factory.LazyAttribute(lambda _: fake.date_between(start_date='today', end_date='+30d'))
#     end_date = factory.LazyAttribute(lambda o: fake.date_between_dates(date_start=o.start_date, date_end=o.start_date + timezone.timedelta(days=7)))
#     status = factory.LazyAttribute(lambda _: fake.random_element(elements=[choice[0] for choice in BookingStatus.choices]))
#     created_at = factory.LazyAttribute(lambda _: timezone.now())
#
#     @classmethod
#     def _create(cls, model_class, *args, **kwargs):
#         # Если renter или offer не переданы, используем существующие
#         if 'renter' not in kwargs:
#             from applications.user.models import User
#             renters = User.objects.filter(role='RENTER')
#             kwargs['renter'] = fake.random_element(renters) if renters.exists() else UserFactory(role='RENTER')
#         if 'offer' not in kwargs:
#             from applications.offers.models import Offer
#             offers = Offer.objects.all()
#             kwargs['offer'] = fake.random_element(offers) if offers.exists() else RentHouseFactory()
#         obj = model_class(*args, **kwargs)
#         obj.save(validate=False)  # Обход валидации дат
#         return obj