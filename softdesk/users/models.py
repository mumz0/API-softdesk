from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.manager import CustomUserManager
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that extends Django's AbstractBaseUser and PermissionsMixin.
    This model provides a custom user implementation with additional fields for
    user consent management and timestamps.
    Attributes:
        created_time (DateTimeField): Timestamp when the user was created (auto-set).
        modified_time (DateTimeField): Timestamp when the user was last modified (auto-updated).
        username (CharField): Unique username for the user (max 150 characters).
        password (CharField): User's password hash (max 128 characters).
        date_of_birth (DateField): User's date of birth.
        can_be_contacted (BooleanField): Whether the user consents to be contacted.
        can_data_be_shared (BooleanField): Whether the user consents to data sharing.
        is_staff (BooleanField): Whether the user can access the admin site.
        is_superuser (BooleanField): Whether the user has all permissions.
        is_active (BooleanField): Whether the user account is active.
    Meta:
        verbose_name: Human-readable name for the model ('user').
        verbose_name_plural: Human-readable plural name for the model ('users').
    Note:
        Uses 'username' as the USERNAME_FIELD for authentication.
        Requires a CustomUserManager to be defined for user management operations.
    """
    
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