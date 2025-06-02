from django.db import models
from django.core.exceptions import ValidationError
from projects.models import Contributor
from users.models import CustomUser

class CustomProjectManager(models.Manager):
    def create_project(self, name, description, type, author):
        """
        Create a new project with the specified details and automatically add the author as a contributor.
        Args:
            name (str): The name of the project.
            description (str): A detailed description of the project.
            type (str): The type/category of the project.
            author (CustomUser): The user who is creating and will be the author of the project.
                               Must be an instance of CustomUser.
        Returns:
            Project: The newly created project instance.
        Raises:
            ValidationError: If the author parameter is not an instance of CustomUser.
        Note:
            This method automatically creates a Contributor record linking the author
            to the project and sets the author as a contributor in the project.
        """
        
        if not isinstance(author, CustomUser):
            raise ValidationError("Author must be an instance of CustomUser.")
        
        project = self.create(name=name, description=description, type=type, author=author, contributors=author)
        Contributor.objects.create(user=author, project=project)
        
        return project
