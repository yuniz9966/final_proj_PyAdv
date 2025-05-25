from django.urls import path
from applications.extra.views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path('', ReviewListCreateView.as_view()),
    path('<int:pk>/', ReviewDetailView.as_view()),
]