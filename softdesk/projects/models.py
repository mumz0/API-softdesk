
from django.utils import timezone
from uuid import uuid4
from django.db import models
from users.models import CustomUser

class CustomProject(models.Model):
    name = models.CharField(unique=True, max_length=150)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    author = models.ForeignKey(CustomUser, related_name='authored_projects', on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'


class Contributor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(CustomProject, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'project')
        

class Issue(models.Model):
    name = models.CharField(max_length=150, default='Default Name')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    priority = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    user = models.ForeignKey(Contributor, related_name='issue_given_to_user', on_delete=models.CASCADE)
    project = models.ForeignKey(CustomProject, related_name='issues', on_delete=models.CASCADE)
    author = models.ForeignKey(Contributor, related_name='created_issues', on_delete=models.CASCADE, null=True, default=None)

    class Meta:
        verbose_name = 'issue'
        verbose_name_plural = 'issues'


class Comment(models.Model):
    author = models.ForeignKey(Contributor, related_name='created_comment', on_delete=models.CASCADE, null=True, default=None)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    issue = models.ForeignKey(Issue, related_name='issue_commented', on_delete=models.CASCADE)
    uuid = models.CharField(max_length=15000)