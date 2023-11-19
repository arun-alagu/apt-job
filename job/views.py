from django.http import JsonResponse
from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

# from core.models import Tag

from job import serializers

from employer.serializers import JobPostSerializer
from job_seeker.serializers import SeekerSkillSetSerializer
from recommender import recommender

from .jobs import jobs

from .permissions import IsNotEmployer, IsEmployer, IsOwner

from core.models import JobPostActivity, SeekerSkillSet, SkillSet, JobPost


class BaseJobAttrViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        return self.queryset.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        """Create a new object"""

        serializer.save(user=self.request.user)


class ListJobPostActivity(generics.ListAPIView):
    serializer_class = serializers.JobPostActivitySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = JobPostActivity.objects.all()
        job = self.request.query_params.get('job')
        if job is not None:
            queryset = queryset.filter(job_post__id=job)
        return queryset


class ListCreateJobPostActivityView(generics.ListCreateAPIView):

    serializer_class = serializers.JobPostActivitySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsNotEmployer)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return JobPostActivity.objects.filter(user=user)

    def perform_create(self, serializer):
        """Create a new object"""

        serializer.save(user=self.request.user)


class RetrieveDestroyJobPostActivityView(generics.RetrieveDestroyAPIView):

    serializer_class = serializers.JobPostActivitySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        user = self.request.user
        return JobPostActivity.objects.filter(user=user)


# class TagViewSet(BaseJobAttrViewSet):
#     """Manage tags in the database"""

#     queryset = Tag.objects.all()
#     serializer_class = serializers.TagSerializer


@api_view(['GET'])
def getJobs(request):
    return Response(jobs)


class SkillsList(generics.ListAPIView):
    """List Skills"""

    queryset = SkillSet.objects.all()
    serializer_class = serializers.SkillSetSerializer


@api_view(['GET'])
def getJob(request, pk):
    for i in jobs:
        if i['id'] == pk:
            job = i
            break
    return Response(job)


@api_view(['GET'])
def getRecommendedJob(request, pk):
    if request.method == 'GET':
        recommendation = recommender.recommender(pk)
        return Response(recommendation)


class JobList(generics.ListAPIView):
    """List Jobs"""

    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer


class SkillsList(generics.ListAPIView):
    """List Jobs"""

    queryset = SeekerSkillSet.objects.all()
    serializer_class = SeekerSkillSetSerializer
