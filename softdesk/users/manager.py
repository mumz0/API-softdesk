from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.exceptions import APIException
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    
    
    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        This method creates a superuser account with default settings appropriate for
        administrative access. It automatically sets required superuser flags and
        provides default values for user consent fields.
        Args:
            username (str): The username for the superuser account.
            password (str, optional): The password for the superuser. Defaults to None.
            **extra_fields: Additional fields to be set on the user model.
        Returns:
            User: The created superuser instance.
        Raises:
            ValueError: If is_staff is not True for the superuser.
            ValueError: If is_superuser is not True for the superuser.
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
        """
        Create and save a new user with the given username and other details.
        Args:
            username (str): The username for the new user. Required field.
            password (str, optional): The password for the user. Defaults to None.
            date_of_birth (date, optional): The user's date of birth. Required field.
            can_be_contacted (bool, optional): Whether the user can be contacted. Defaults to None.
            can_data_be_shared (bool, optional): Whether the user's data can be shared. Defaults to None.
            **extra_fields: Additional fields to be set on the user model.
        Returns:
            User: The created user instance.
        Raises:
            ValidationError: If username or date_of_birth is not provided.
            APIException: If the user is under 15 years old (HTTP 400).
        Note:
            The minimum age requirement is 15 years. Age is calculated based on the 
            difference between current date and date_of_birth.
        """
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
        """
        Update a user instance with the provided field values.

        Args:
            user: The user instance to be updated.
            **kwargs: Arbitrary keyword arguments representing field-value pairs
                     to update on the user instance.
        Returns:
            None
        """
        for field, value in kwargs.items():
            setattr(user, field, value)
        user.save()
    

    def delete_user(self, user):
        """
        Delete a user from the database.

        Args:
            user: The user instance to be deleted from the database.
        Raises:
            DatabaseError: If the deletion operation fails due to database constraints.
            AttributeError: If the user object doesn't have a delete method.
        """
        user.delete()
    

    def read_user(self, user):
        """
        Return the provided user object without modification.

        Args:
            user: The user object to be returned.
        Returns:
            The same user object that was passed as input.
        """
        return user