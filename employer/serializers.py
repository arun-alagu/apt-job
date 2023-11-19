from rest_framework import serializers

from core.models import BusinessStream, CompanyLocation, CompanyProfile, JobPost


class BusinessStreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessStream
        fields = '__all__'
        read_only_fields = ('id', 'user')


class CompanyLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyLocation
        fields = '__all__'
        read_only_fields = ('id', 'user')


class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = '__all__'
        read_only_fields = ('id', 'user',)


class JobPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobPost
        fields = '__all__'
        read_only_fields = ('id', 'user',)
