from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from django.contrib.auth import get_user_model

from user.serializers import (
    UserAccountManageSerializer,
    UserSerializer,
    MyTokenObtainPairSerializer,
    UserSerializerWithToken,
    EmployerSerializerWithToken
)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializerWithToken


class CreateEmployerView(generics.CreateAPIView):
    """Create a new user in the system"""
    queryset = get_user_model().objects.all()
    serializer_class = EmployerSerializerWithToken

# class CreateTokenView(ObtainAuthToken):
#     """Create a new auth token for user"""

#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserAccountManageSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""

        return self.request.user


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
