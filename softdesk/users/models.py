from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.manager import CustomUserManager
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    username = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    can_be_contacted = models.BooleanField()
    can_data_be_shared = models.BooleanField()
    is_staff = models.BooleanField(default= False)
    is_superuser = models.BooleanField(default= False)
    is_active = models.BooleanField(default= True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'