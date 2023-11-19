from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.decorators import api_view

from core.models import (
    BusinessStream, CompanyLocation, CompanyProfile, JobPost)
from employer import serializers

from rest_framework_simplejwt.authentication import JWTAuthentication


from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsSuperUser, IsEmployer, IsOwner

# Create your views here.


class BusinessStreamViewSet(ModelViewSet):

    queryset = BusinessStream.objects.all()
    serializer_class = serializers.BusinessStreamSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsOwner, ]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwner, ]
        elif self.action == 'create':
            self.permission_classes = [IsEmployer, ]
        elif self.action == 'update':
            self.permission_classes = [IsEmployer, ]
        elif self.action == 'partial_update':
            self.permission_classes = [IsEmployer, ]
        elif self.action == 'delete':
            self.permission_classes = [IsEmployer, ]
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        queryset = BusinessStream.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CompanyLocationViewSet(ModelViewSet):

    queryset = CompanyLocation.objects.all()
    serializer_class = serializers.CompanyLocationSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsOwner, ]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwner, ]
        elif self.action == 'create':
            self.permission_classes = [IsEmployer, ]
        elif self.action == 'update':
            self.permission_classes = [IsEmployer, ]
        elif self.action == 'partial_update':
            self.permission_classes = [IsEmployer, ]
        elif self.action == 'delete':
            self.permission_classes = [IsEmployer, ]
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        queryset = CompanyLocation.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CompanyProfileViewSet(ModelViewSet):

    queryset = BusinessStream.objects.all()
    serializer_class = serializers.CompanyProfileSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        queryset = CompanyProfile.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class JobsViewSet(ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = serializers.JobPostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'job_title', 'job_location']
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id', 'job_title']


# class JobList(generics.ListAPIView):
#     """List Jobs"""

#     queryset = JobPost.objects.all()
#     serializer_class = serializers.JobPostSerializer


@api_view(['GET'])
def JobList(request):
    query = request.query_params.get('job')
    locQuery = request.query_params.get('loc')
    if query == None:
        query = ''
    if locQuery == None:
        locQuery = ''

    jobs = JobPost.objects.filter(
        job_title__icontains=query, job_location__icontains=locQuery).order_by('-created_date')

    page = request.query_params.get('page')
    paginator = Paginator(jobs, 4)

    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = serializers.JobPostSerializer(jobs, many=True)
    return Response({'jobs': serializer.data, 'page': page, 'pages': paginator.num_pages})


class JobDetails(generics.RetrieveAPIView):
    "Reterieve Jobs"

    queryset = JobPost.objects.all()
    serializer_class = serializers.JobPostSerializer


class ListCreateJobPostView(generics.ListCreateAPIView):
    "Create Jobs"
    serializer_class = serializers.JobPostSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsEmployer)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return JobPost.objects.filter(user=user)

    def perform_create(self, serializer):
        """Create a new object"""

        serializer.save(user=self.request.user)


class ManageJobPostView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.JobPostSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return JobPost.objects.filter(user=user)


# class BusinessStreamCreateList(generics.ListCreateAPIView):

#     queryset = BusinessStream.objects.all()
#     serializer_class = serializers.BusinessStreamSerializer
#     authentication_classes = (JWTAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)

#     def perform_create(self, serializer):
#         return serializer.save(user=self.request.user)
