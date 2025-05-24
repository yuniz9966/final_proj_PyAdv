from django.urls import path
from applications.extra.views import ReviewListCreateView

urlpatterns = [
    path('', ReviewListCreateView.as_view()),
]