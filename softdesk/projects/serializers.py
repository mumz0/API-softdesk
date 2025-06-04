from rest_framework import serializers

from .models import CustomProject, Contributor, Issue, Comment

class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model.

    This serializer handles the serialization and deserialization of Contributor
    instances, including the id, user, project, and created_time fields.

    Fields:
        id: The unique identifier of the contributor
        user: The user who is a contributor to the project
        project: The project to which the user is contributing
        created_time: The timestamp when the contributor was added to the project
    """
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']


class CustomProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomProject model.
    This serializer handles the serialization and deserialization of CustomProject
    instances, providing a JSON representation of project data.
    Fields:
        id (int): Unique identifier for the project (read-only)
        name (str): Name of the project
        description (str): Detailed description of the project
        type (str): Type/category of the project
        author (User): User who created the project (read-only)
    Read-only fields:
        - id: Auto-generated primary key
        - author: Set automatically based on the authenticated user
        - created_time: Timestamp when the project was created
        - modified_time: Timestamp when the project was last modified
    Note:
        The author field is automatically populated and cannot be modified
        through this serializer to ensure data integrity.
    """

    class Meta:
        model = CustomProject
        fields = ['id', 'name', 'description', 'type', 'author']
        read_only_fields = ["id", "author", 'created_time', 'modified_time']
        
        
class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for Issue model.

    This serializer handles the serialization and deserialization of Issue instances
    for API operations. It includes all essential fields while protecting certain
    fields from modification through the API.

    Fields:
        - id: Unique identifier for the issue (read-only)
        - name: Title or name of the issue
        - description: Detailed description of the issue
        - status: Current status of the issue
        - priority: Priority level of the issue
        - type: Type/category of the issue
        - user: User who created the issue (read-only)
        - project: Project the issue belongs to (read-only)
        - created_time: Timestamp when issue was created (read-only)
        - modified_time: Timestamp when issue was last modified (read-only)

    Read-only fields:
        Fields that cannot be modified through API requests to maintain data integrity
        and proper assignment of ownership and timestamps.
    """
    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'status', 'priority', 'type', 'user', 'project']
        read_only_fields = ["id", "project", 'created_time', 'modified_time']
        
        
class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.

    This serializer handles the serialization and deserialization of Comment instances.
    It includes all relevant fields for comment data while protecting certain fields
    from modification through the API.

    Fields:
        - id: Unique identifier for the comment (read-only)
        - author: User who created the comment (read-only)
        - created_time: Timestamp when comment was created (read-only)
        - modified_time: Timestamp when comment was last modified (read-only)
        - description: Content of the comment (editable)
        - issue: Associated issue for the comment (read-only)
        - uuid: Unique identifier UUID for the comment (read-only)

    Read-only fields are automatically set by the system and cannot be modified
    through API requests.
    """
    class Meta:
        model = Comment
        fields = ['id','author', 'created_time', 'modified_time', 'description', 'issue', 'uuid']
        read_only_fields = ["id", "author", 'created_time', 'modified_time', "uuid", "issue"]

