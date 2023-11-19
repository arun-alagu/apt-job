from urllib import request
from rest_framework import generics, authentication, permissions

from django.conf import settings
from django.contrib.auth import get_user_model

from core.models import EducationDetail, ExperienceDetail, JobPost, SeekerProfile, SeekerSkillSet
from job.permissions import IsEmployer

from job_seeker import serializers

from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsNotEmployer, IsOwner, IsSuperUser

from employer.serializers import JobPostSerializer


# class CreateUserProfileView(generics.CreateAPIView):

#     queryset = SeekerProfile.objects.all()
#     serializer_class = serializers.ProfileSerializer
#     authentication_classes = (JWTAuthentication,)
#     permission_classes = (permissions.IsAuthenticated, IsNotEmployer)

#     def perform_create(self, serializer):
#         return serializer.save(user=self.request.user)


class ListCreateUserProfileView(generics.ListCreateAPIView):
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsNotEmployer)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return SeekerProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        """Create a new object"""

        serializer.save(user=self.request.user)


class ManageUserProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = serializers.ProfileSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return SeekerProfile.objects.filter(user=user)


class RetrieveUserProfileView(generics.ListAPIView):

    serializer_class = serializers.ProfileSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsEmployer)
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        # queryset = SeekerProfile.objects.all()
        # user = self.request.query_params.get('user')
        # if user is not None:
        #     queryset = queryset.filter(user__id=user)
        # return queryset

        id_list = self.request.GET.getlist("user")[0].split(',')
        map_object = map(int, id_list)
        id_list = list(map_object)
        if not id_list:
            return []
        objects = SeekerProfile.objects.filter(user__in=id_list)
        print(objects)
        objects = dict([(obj.user_id, obj) for obj in objects])
        print(objects)
        sorted_objects = [objects[user_id] for user_id in id_list]
        return sorted_objects


class ListCreateEducationDetailView(generics.ListCreateAPIView):
    """List Educations"""

    serializer_class = serializers.EducationDetailSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsNotEmployer)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return EducationDetail.objects.filter(user=user)

    def perform_create(self, serializer):
        """Create a new object"""

        serializer.save(user=self.request.user)


class ManageEducationDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.EducationDetailSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return EducationDetail.objects.filter(user=user)


class ListCreateSeekerSkillSetView(generics.ListCreateAPIView):
    """List Educations"""

    serializer_class = serializers.SeekerSkillSetSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsNotEmployer)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return SeekerSkillSet.objects.filter(user=user)

    def perform_create(self, serializer):
        """Create a new object"""

        serializer.save(user=self.request.user)


class ManageSeekerSkillSetView(generics.RetrieveUpdateAPIView):

    serializer_class = serializers.SeekerSkillSetSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return SeekerSkillSet.objects.filter(user=user)


class ListCreateExperienceDetailView(generics.ListCreateAPIView):
    """List Educations"""

    serializer_class = serializers.ExperienceDetailSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsNotEmployer)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return ExperienceDetail.objects.filter(user=user)

    def perform_create(self, serializer):
        """Create a new object"""

        serializer.save(user=self.request.user)


class ManageExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.ExperienceDetailSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return ExperienceDetail.objects.filter(user=user)


# class userProfileDetail(generics.RetrieveUpdateAPIView):

#     queryset = SeekerProfile.objects.all()
#     serializer_class = serializers.ProfileSerializer
#     authentication_classes = (JWTAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_serializer_class(self):

#         return self.queryset.filter(user=self.request.user)


class UserProfileViewSet(ModelViewSet):

    queryset = SeekerProfile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwner]
        elif self.action == 'create':
            self.permission_classes = [IsNotEmployer]
        elif self.action == 'update':
            self.permission_classes = [IsOwner]
        elif self.action == 'partial_update':
            self.permission_classes = [IsOwner]
        elif self.action == 'delete':
            self.permission_classes = [IsOwner]
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        queryset = SeekerProfile.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_object(self):
        """Retrieve and return authentication user"""

        return self.request.user


class AppliedJobsList(generics.ListAPIView):
    serializer_class = JobPostSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsNotEmployer,)
    filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('id',)

    def get_queryset(self):
        id_list = self.request.GET.getlist("id")[0].split(',')
        map_object = map(int, id_list)
        id_list = list(map_object)
        # print(id_list)
        if not id_list:
            return []
        objects = JobPost.objects.filter(id__in=id_list)
        print(objects)
        objects = dict([(obj.id, obj) for obj in objects])
        sorted_objects = [objects[id] for id in id_list]
        # print(sorted_objects)
        return sorted_objects

    # def perform_update(self, serializer):
    #     return serializer.save(user=self.request.user)


# class userProfileList(
#         mixins.ListModelMixin,
#         mixins.CreateModelMixin,
#         generics.GenericAPIView):

#     queryset = SeekerProfile.objects.all()
#     serializer_class = serializers.ProfileSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request):
#         return self.list(request)

#     def post(self, request):
#         self.user = request.user
#         return self.create(request)

# class userProfileDetail (
#         mixins.RetrieveModelMixin,
#         mixins.UpdateModelMixin,
#         mixins.DestroyModelMixin,
#         generics.GenericAPIView):

#     queryset = SeekerProfile.objects.all()
#     serializer_class = serializers.ProfileSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, pk):
#         return self.retrieve(request, pk)

#     def put(self, request, pk):
#         return self.update(request, pk)

#     def delete(self, request, pk):
#         return self.destroy(request, pk)
