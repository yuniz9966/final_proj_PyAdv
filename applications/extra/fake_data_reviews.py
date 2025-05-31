import factory
from faker import Faker
from django.utils import timezone
from applications.extra.model_reviews import Review
from applications.user.fake_data_user import UserFactory
from applications.offers.fake_data_offers import RentHouseFactory

fake = Faker("de_DE")

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    author = factory.SubFactory(UserFactory, role='RENTER')
    offer = factory.SubFactory(RentHouseFactory)
    rating = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=5))
    comment = factory.LazyAttribute(lambda _: fake.paragraph(nb_sentences=3))
    created_at = factory.LazyAttribute(lambda _: timezone.now())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Если author или offer не переданы, используем существующие
        if 'author' not in kwargs:
            from applications.user.models import User
            renters = User.objects.filter(role='RENTER')
            kwargs['author'] = fake.random_element(renters) if renters.exists() else UserFactory(role='RENTER')
        if 'offer' not in kwargs:
            from applications.offers.models import Offer
            offers = Offer.objects.all()
            kwargs['offer'] = fake.random_element(offers) if offers.exists() else RentHouseFactory()
        return super()._create(model_class, *args, **kwargs)