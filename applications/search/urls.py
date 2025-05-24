from django.urls import path
from applications.search.views import SearchListView

urlpatterns = [
    path('', SearchListView.as_view()),
]