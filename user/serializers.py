from ast import Pass
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users object"""

    isEmployer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name", 'isEmployer']
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def get_isEmployer(self, obj):

        return obj.is_staff

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, with encrypted password and return it"""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserSerializerWithToken(UserSerializer):
    """Serializer for user login"""

    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name", 'isEmployer', 'token']
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


# class EmployerSerializer(serializers.ModelSerializer):

#     isEmployer = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = get_user_model()
#         fields = ["email", "password", "name", 'isEmployer']
#         extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

#     def get_isEmployer(self, obj):

#         return obj.is_staff

#     def create(self, validated_data):
#         """Create a new user with encrypted password and return it"""

#         return get_user_model().objects.create_staffuser(**validated_data)

#     def update(self, instance, validated_data):
#         """Update a user, with encrypted password and return it"""

#         password = validated_data.pop('password', None)
#         user = super().update(instance, validated_data)

#         if password:
#             user.set_password(password)
#             user.save()

#         return user


class EmployerSerializerWithToken(serializers.ModelSerializer):

    isEmployer = serializers.SerializerMethodField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name", 'isEmployer', 'token']
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def get_isEmployer(self, obj):

        return obj.is_staff

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        return get_user_model().objects.create_staffuser(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, with encrypted password and return it"""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class UserAccountManageSerializer(serializers.ModelSerializer):
    """Serializer to view user account details"""

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, "min_length": 8}}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


# class AuthTokenSerializer(serializers.Serializer):
#     """ Serializer for the user authentiation object"""

#     email = serializers.CharField()
#     password = serializers.CharField(
#         style={'input_type': 'password'},
#         trim_whitespace=False
#     )

#     def validate(self, attrs):
#         """Validate and authenticate the user"""

#         email = attrs.get('email')
#         password = attrs.get('password')

#         user = authenticate(
#             request=self.context.get('request'),
#             username=email,
#             password=password
#         )

#         if not user:
#             msg = _("Unable to authenticate with provided credentials")
#             raise serializers.ValidationError(msg, code='authentication')

#         attrs['user'] = user
#         return attrs
