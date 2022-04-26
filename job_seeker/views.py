from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import EducationDetail

from job_seeker import serializers


class EducationDetailViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin
    ):
    """Manage education details in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = EducationDetail.objects.all()
    serializer_class = serializers.EducationDetailSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user"""

        return self.queryset.filter(user=self.request.user).order_by('-id')