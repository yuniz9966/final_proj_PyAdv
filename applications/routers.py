from django.urls import path, include

urlpatterns = [
    path('users/', include('applications.user.urls')),
    path('offers/', include('applications.offers.urls')),
    path('bookings/', include('applications.bookings.urls')),
    path('search/', include('applications.search.urls')),
    path('reviews/', include('applications.extra.urls'))
]