from rest_framework import serializers

from core.models import EducationDetail

class EducationDetailSerializer(serializers.ModelSerializer):
    """Serializer for education detail objects"""

    class Meta:
        model = EducationDetail
        fields = (
            "certified_degree_name",
            "major",
            "institute_university_name",
            "start_year",
            "complete_year",
            "percentage",
            "cgpa"
        )
        read_only_fields = ("id",)
