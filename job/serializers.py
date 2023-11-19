from rest_framework import serializers

from core.models import JobPostActivity, SkillSet

# from core.models import Tag


# class TagSerializer(serializers.ModelSerializer):
#     """Serializer for tag objects"""

#     class Meta:
#         model = Tag
#         fields = ('id', 'name')
#         read_only_fields = ('id',)

class SkillSetSerializer(serializers.ModelSerializer):
    """serializer fro skill set"""

    class Meta:
        model = SkillSet
        fields = '__all__'
        read_only_fields = ('id', 'skill_set_name')


class JobPostActivitySerializer(serializers.ModelSerializer):
    """serializer fro job post activity set"""

    class Meta:
        model = JobPostActivity
        fields = '__all__'
        read_only_fields = ('id', 'user',)
