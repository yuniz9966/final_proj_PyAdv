from django.urls import path
from applications.offers.views import (
    OfferListCreateView,
    OfferDetailView,
    OfferToggleStatusView,
    MyOffersView,
)

urlpatterns = [
    path('create/', OfferListCreateView.as_view()),
    path('<int:pk>/', OfferDetailView.as_view()),
    path('<int:pk>/toggle-status/', OfferToggleStatusView.as_view()),
path('offers/my/', MyOffersView.as_view()),
]