from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from applications.user.views import RegisterView, UserListView, LogoutView

urlpatterns = [
    path('list/', UserListView.as_view()),
    path('register/', RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
]
