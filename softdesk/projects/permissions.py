from rest_framework import permissions

from projects.models import Contributor, CustomProject

class CommentPermissions(permissions.BasePermission):
    
    
    def has_permission(self, request, view):
    
        project_id = view.kwargs.get('project_id')
        project = CustomProject.objects.get(pk=project_id)
        return Contributor.objects.filter(project=project, user=request.user).exists()
        
        
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user