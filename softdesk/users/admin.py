from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, UserAdmin)