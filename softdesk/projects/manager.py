from django.db import models
from django.core.exceptions import ValidationError
from projects.models import Contributor
from users.models import CustomUser

class CustomProjectManager(models.Manager):
    def create_project(self, name, description, type, author):
        
        if not isinstance(author, CustomUser):
            raise ValidationError("Author must be an instance of CustomUser.")
        
        project = self.create(name=name, description=description, type=type, author=author, contributors=author)
        Contributor.objects.create(user=author, project=project)
        
        return project
