import factory
from faker import Faker
from django.utils import timezone
from applications.extra.model_reviews import Review
from applications.user.fake_data_user import UserFactory
from applications.offers.fake_data_offers import RentHouseFactory
from applications.bookings.models import Booking, BookingStatus

fake = Faker("de_DE")

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    author = factory.SubFactory(UserFactory, role='RENTER')
    offer = factory.SubFactory(RentHouseFactory)
    rating = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=5))
    comment = factory.LazyAttribute(lambda _: fake.paragraph(nb_sentences=3))
    created_at = factory.LazyAttribute(lambda _: timezone.now())

    @factory.post_generation
    def create_booking(self, create, extracted, **kwargs):
        if create:
            Booking.objects.create(
                renter=self.author,
                offer=self.offer,
                start_date=fake.date_between(start_date='today', end_date='+30d'),
                end_date=fake.date_between(start_date='+31d', end_date='+60d'),
                status=BookingStatus.CONFIRMED
            )