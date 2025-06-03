from rest_framework import generics
from applications.user.models import User
from applications.user.serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from datetime import datetime, timezone
from django.contrib.auth import get_user_model

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        # username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"detail": "Недействительные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        access_expiry = datetime.fromtimestamp(access_token['exp'], tz=timezone.utc)
        refresh_expiry = datetime.fromtimestamp(refresh['exp'], tz=timezone.utc)

        response = Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=str(access_token),
            httponly=True,
            samesite='Lax',
            secure=False,  # change to True in production with HTTPS
            expires=access_expiry
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            samesite='Lax',
            secure=False,
            expires=refresh_expiry
        )

        return response


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass  # можно логировать

        response = Response({"detail": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
