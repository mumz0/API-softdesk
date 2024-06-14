from rest_framework import serializers
from .models import CustomProject, Contributor, Issue, Comment

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']


class CustomProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = CustomProject
        fields = ['id', 'name', 'description', 'type', 'author', 'contributors']
        read_only_fields = ["id", "author", 'created_time', 'modified_time']
        
        
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'status', 'priority', 'type', 'user', 'project']
        read_only_fields = ["id", "user", "project", 'created_time', 'modified_time']
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','author', 'created_time', 'modified_time', 'description', 'issue', 'uuid']
        read_only_fields = ["id", "author", 'created_time', 'modified_time', "uuid"]