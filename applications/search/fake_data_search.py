import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.utils import timezone
import json
from applications.search.models import SearchQuery
from applications.user.fake_data_user import UserFactory
from applications.offers.choices.room_type import RoomType

fake = Faker("de_DE")

class SearchQueryFactory(DjangoModelFactory):
    class Meta:
        model = SearchQuery

    user = factory.SubFactory(UserFactory)
    query = factory.LazyAttribute(lambda _: fake.word())
    filters = factory.LazyAttribute(
        lambda _: json.dumps({
            'city': fake.city(),
            'min_price': fake.random_int(min=300, max=800),
            'max_price': fake.random_int(min=800, max=1500),
            'rooms_count': fake.random_int(min=1, max=5),
            'room_type': fake.random_element(elements=[choice[0] for choice in RoomType.choices()])
        })
    )
    created_at = factory.LazyAttribute(lambda _: timezone.now())

    @factory.post_generation
    def set_user(self, create, extracted, **kwargs):
        if not create:
            return
        self.user = None if fake.random_element(elements=(True, False)) else self.user
        self.save()