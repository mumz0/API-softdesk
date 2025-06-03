
from django.db.models import SET_NULL
from uuid import uuid4
from django.db import models
from users.models import CustomUser

class CustomProject(models.Model):
    """
    Django model representing a software development project.
    This model stores information about projects including their type (Backend, Frontend, iOS, Android),
    basic metadata, and author relationship.
    Attributes:
        TYPE_CHOICES (list): Available project types with display names
        name (CharField): Unique project name, max 150 characters
        created_time (DateTimeField): Timestamp when project was created (auto-generated)
        modified_time (DateTimeField): Timestamp when project was last modified (auto-updated)
        description (CharField): Project description, max 150 characters
        type (CharField): Project type from TYPE_CHOICES, max 150 characters
        author (ForeignKey): Reference to CustomUser who created the project
    Methods:
        __str__(): Returns the project name as string representation
    Meta:
        verbose_name: 'project'
        verbose_name_plural: 'projects'
    """
    TYPE_CHOICES = [
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android')
    ]
    name = models.CharField(unique=True, max_length=150)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=150)
    type = models.CharField(max_length=150, choices=TYPE_CHOICES)
    author = models.ForeignKey(CustomUser, related_name='authored_projects', on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'


class Contributor(models.Model):
    """
    Model representing the relationship between users and projects.
    A Contributor represents a user who has been added to a specific project,
    establishing a many-to-many relationship between CustomUser and CustomProject.
    Attributes:
        user (ForeignKey): Reference to the CustomUser who is contributing to the project.
        project (ForeignKey): Reference to the CustomProject that the user is contributing to.
        created_time (DateTimeField): Timestamp when the contributor was added to the project.
                                     Automatically set when the record is created.
    Meta:
        unique_together: Ensures that a user can only be added once to a specific project,
                        preventing duplicate contributor entries for the same user-project pair.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(CustomProject, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'project')
        

class Issue(models.Model):
    """
    Django model representing an issue within a project management system.
    An Issue is a work item that can be assigned to contributors within a project.
    It tracks bugs, features, or tasks with associated metadata like priority,
    status, and assignment information.
    Attributes:
        name (CharField): The title/name of the issue with a maximum length of 150 characters.
            Defaults to 'Default Name'.
        created_time (DateTimeField): Timestamp when the issue was created.
            Automatically set on creation.
        modified_time (DateTimeField): Timestamp when the issue was last modified.
            Automatically updated on save.
        description (CharField): Detailed description of the issue with a maximum
            length of 150 characters.
        status (CharField): Current status of the issue. Choices are 'TO_DO',
            'IN_PROGRESS', or 'FINISHED'. Defaults to 'TO_DO'.
        priority (CharField): Priority level of the issue. Choices are 'LOW',
            'MEDIUM', or 'HIGH'. Defaults to 'LOW'.
        type (CharField): Type of issue. Choices are 'BUG', 'FEATURE', or 'TASK'.
        user (ForeignKey): The contributor assigned to work on this issue.
            Related to Contributor model with CASCADE deletion.
        project (ForeignKey): The project this issue belongs to.
            Related to CustomProject model with CASCADE deletion.
        author (ForeignKey): The contributor who created this issue.
            Related to Contributor model with CASCADE deletion. Can be null.
    Meta:
        verbose_name: 'issue'
        verbose_name_plural: 'issues'
    Relationships:
        - Many-to-one with Contributor (user): issue_given_to_user
        - Many-to-one with CustomProject: issues
        - Many-to-one with Contributor (author): created_issues
    """
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'), 
        ('HIGH', 'High')
    ]
    
    STATUS_CHOICES = [
        ('TO_DO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished')
    ]
    TYPE_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task')
    ]

    name = models.CharField(max_length=150, default='Default Name')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=150)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES, default='TO_DO')
    priority = models.CharField(max_length=150, choices=PRIORITY_CHOICES, default='LOW')
    type = models.CharField(max_length=150, choices=TYPE_CHOICES)
    user = models.ForeignKey(Contributor, related_name='issue_given_to_user', on_delete=models.CASCADE)
    project = models.ForeignKey(CustomProject, related_name='issues', on_delete=models.CASCADE)
    author = models.ForeignKey(Contributor, related_name='created_issues', on_delete=models.CASCADE, null=True, default=None)

    class Meta:
        verbose_name = 'issue'
        verbose_name_plural = 'issues'


class Comment(models.Model):
    """
    Model representing a comment on an issue within a project.
    A comment is created by a user (author) and is associated with a specific issue.
    Comments include a description, timestamps for creation and modification,
    and a unique identifier.
    Attributes:
        author (ForeignKey): The user who created the comment.
            Related name: 'created_comments'
        created_time (DateTimeField): Timestamp when the comment was created.
            Automatically set on creation.
        modified_time (DateTimeField): Timestamp when the comment was last modified.
            Automatically updated on save.
        description (CharField): The content of the comment (max 150 characters).
        issue (ForeignKey): The issue this comment belongs to.
            Related name: 'issue_commented'
        uuid (UUIDField): Unique identifier for the comment.
            Automatically generated and not editable.
    Meta:
        verbose_name: 'comment'
        verbose_name_plural: 'comments'
    """
    author = models.ForeignKey(CustomUser, related_name='created_comments', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=150)
    issue = models.ForeignKey(Issue, related_name='issue_commented', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, editable=False)
    
    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        
