from django.contrib import admin
from users.admin import UserAdmin
from .models import Contributor, CustomProject, Issue
from django.contrib import admin
from .models import CustomProject, Contributor, Issue, Comment


class IssueAdmin(admin.ModelAdmin):
    pass

        
admin.site.register(CustomProject, UserAdmin)
admin.site.register(Contributor, UserAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, UserAdmin)