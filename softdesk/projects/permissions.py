from rest_framework import permissions

from projects.models import Contributor, CustomProject

class ProjectPermissions(permissions.BasePermission):
    
    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the requested action on a project.
        This permission class allows:
        - POST requests for all authenticated users (project creation)
        - Other HTTP methods only for users who are contributors to the specific project
        Args:
            request: The HTTP request object containing user information
            view: The view object containing URL parameters (pk or project_id)
        Returns:
            bool: True if the user has permission, False otherwise
        Notes:
            - For POST requests, permission is always granted (assuming authentication)
            - For other methods, requires the user to be a contributor of the project
            - Returns False if the project doesn't exist
            - Returns True if no project_id is found in the URL parameters
        """
        if request.method == 'POST':
            return True  
        
        project_id = view.kwargs.get('pk') or view.kwargs.get('project_id')
        if project_id:
            try:
                project = CustomProject.objects.get(pk=project_id)
                return Contributor.objects.filter(project=project, user=request.user).exists()
            except CustomProject.DoesNotExist:
                return False
        return True
        
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the requested action on the project object.

        For safe methods (GET, HEAD, OPTIONS), users need to be contributors of the project.
        For unsafe methods (POST, PUT, PATCH, DELETE), only the project author has permission.

        Args:
            request: The HTTP request object containing user and method information
            view: The view that is handling the request
            obj: The project object being accessed

        Returns:
            bool: True if the user has permission, False otherwise
        """
        if request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(project=obj, user=request.user).exists()
        return obj.author == request.user
    
class CommentPermissions(permissions.BasePermission):
    
    
    def has_permission(self, request, view):
        """
        Check if the current user has permission to access the project.
        This method verifies that the requesting user is a contributor to the specified project.
        It retrieves the project using the project_id from the view's URL parameters and checks
        if there exists a Contributor relationship between the user and the project.
        Args:
            request (HttpRequest): The HTTP request object containing user information.
            view (ViewSet): The view instance containing URL parameters including 'project_id'.
        Returns:
            bool: True if the user is a contributor to the project, False otherwise.
        Raises:
            CustomProject.DoesNotExist: If no project exists with the given project_id.
        """
    
        project_id = view.kwargs.get('project_id')
        project = CustomProject.objects.get(pk=project_id)
        return Contributor.objects.filter(project=project, user=request.user).exists()
        
        
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the requested action on the object.
        Args:
            request: The HTTP request object containing user information and method type.
            view: The view that is handling the request.
            obj: The object instance that the permission check is being performed on.
        Returns:
            bool: True if the user has permission to perform the action, False otherwise.
                  - Returns True for safe methods (GET, HEAD, OPTIONS) for all users
                  - Returns True for unsafe methods (POST, PUT, PATCH, DELETE) only if 
                    the requesting user is the author of the object
        """
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
    