from rest_framework import serializers

from core.models import EducationDetail

class EducationDetailSerializer(serializers.ModelSerializer):
    """Serializer for education detail objects"""

    class Meta:
        model = EducationDetail
        fields = '__all__' 
        read_only_fields = ['id']
