from rest_framework import serializers
from .models import CustomProject, Contributor, Issue

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']

class CustomProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = CustomProject
        fields = ['id', 'name', 'description', 'type', 'author', 'contributors']
        read_only_fields = ["id", "author"]
        
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'status', 'priority', 'type', 'user', 'project']
        read_only_fields = ["id", "user", "project"]