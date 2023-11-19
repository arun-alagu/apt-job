from rest_framework import serializers

from core.models import(ExperienceDetail, SeekerProfile,
                        EducationDetail, SeekerSkillSet)


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user Profile"""

    class Meta:
        model = SeekerProfile
        fields = '__all__'
        read_only_fields = ('id', 'user')


class EducationDetailSerializer(serializers.ModelSerializer):
    """Serializer for education detail objects"""

    class Meta:
        model = EducationDetail
        fields = '__all__'
        read_only_fields = ('id', 'user',)


class SeekerSkillSetSerializer(serializers.ModelSerializer):
    """Serializer for education detail objects"""

    class Meta:
        model = SeekerSkillSet
        fields = '__all__'
        read_only_fields = ('id', 'user',)


class ExperienceDetailSerializer(serializers.ModelSerializer):
    """Serializer for education detail objects"""

    class Meta:
        model = ExperienceDetail
        fields = '__all__'
        read_only_fields = ('id', 'user',)
