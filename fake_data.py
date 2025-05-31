import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FINAL_PROJECT_PyAdv.settings')
django.setup()

def populate_db():
    from applications.user.fake_data_user import UserFactory
    from applications.offers.fake_data_offers import LocationFactory, RentHouseFactory
    from applications.bookings.fake_data_bookings import BookingFactory
    from applications.search.fake_data_search import SearchQueryFactory
    from applications.extra.fake_data_reviews import ReviewFactory


    UserFactory.create_batch(3, role='RENTER')
    UserFactory.create_batch(3, role='OWNER')
    print("Created 10 users")

    LocationFactory.create_batch(5)
    print("Created 10 locations")

    RentHouseFactory.create_batch(10, owner__role='OWNER')
    print("Created 20 offers")

    BookingFactory.create_batch(5, status='CONFIRMED')
    print("Created 15 bookings")

    SearchQueryFactory.create_batch(5)
    print("Created 10 search queries")

    ReviewFactory.create_batch(5)
    print("Created 10 reviews")

if __name__ == "__main__":
    populate_db()