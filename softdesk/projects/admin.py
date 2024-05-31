from django.contrib import admin
from users.admin import UserAdmin
from .models import Contributor, CustomProject, Issue
from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from .models import CustomProject, Contributor, Issue




class IssueAdmin(admin.ModelAdmin):
    list_display = ('user','name','status', 'priority', 'type', 'project')
    
    def save_model(self, request, obj, form, change):
        # Check if the user is a contributor to the project
        if not Contributor.objects.filter(user=obj.user, project=obj.project).exists():
            self.message_user(request, "The user must be a contributor to the project to create an issue.", level='error')
            return HttpResponseForbidden("The user must be a contributor to the project to create an issue.")
        
        # Check if the issue description already exists in the project
        if Issue.objects.filter(name=obj.name, project=obj.project).exists():
            self.message_user(request, "An issue with this name already exists in this project.", level='error')
            return HttpResponseBadRequest("An issue with this name already exists in this project.")
        
        super().save_model(request, obj, form, change)

        
        
admin.site.register(CustomProject, UserAdmin)
admin.site.register(Contributor, UserAdmin)
admin.site.register(Issue, IssueAdmin)