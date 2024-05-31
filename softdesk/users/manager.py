from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.exceptions import APIException
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    
    
    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("can_be_contacted", False)
        extra_fields.setdefault("can_data_be_shared", False)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        date_of_birth = (datetime.now() - timedelta(days=16 * 365)).date()

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        return self.create_user(username, password, date_of_birth, **extra_fields)
        
        
    def create_user(self, username, password=None, date_of_birth=None, can_be_contacted=None, can_data_be_shared=None, **extra_fields):
        
        
        if not username:
            raise ValidationError({'username': ['Le champ "username" doit être renseigné']})
        
        if not date_of_birth:
            raise ValidationError({'date_of_birth': ['Le champ "date of birth" doit être renseigné']})
        
        age = (datetime.now().date() - date_of_birth).days // 365

        if age < 15:
            raise APIException("Vous devez avoir au moins 15 ans pour vous inscrire.", code=status.HTTP_400_BAD_REQUEST)

        user = self.model(username=username, date_of_birth=date_of_birth, can_be_contacted=can_be_contacted, can_data_be_shared=can_data_be_shared, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def update_user(self, user, **kwargs):
        for field, value in kwargs.items():
            setattr(user, field, value)
        user.save()
    

    def delete_user(self, user):
        user.delete()
    

    def read_user(self, user):
        return user