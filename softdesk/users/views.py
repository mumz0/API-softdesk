from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from users.models import CustomUser
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status


class CreateUserAPIView(APIView):
    """
    API view for creating new user accounts.
    This view handles POST requests to create a new user using the UserSerializer.
    Validates the provided user data and creates a new user instance if valid.
    Methods:
        post(request): Creates a new user account with the provided data.
    Returns:
        Response: JSON response with user data and 201 status on success,
                  or validation errors with 400 status on failure.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):
    
    def get_object(self, pk):
        """
        Retrieve a CustomUser instance by primary key.

        Args:
            pk: The primary key of the user to retrieve.
        Returns:
            CustomUser: The user instance with the specified primary key.
        Raises:
            Http404: If no user exists with the given primary key.
        """
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    
    def put(self, request, pk):
        """
        Update an existing user with the provided data.

        Args:
            request: HTTP request object containing user data to update
            pk: Primary key of the user to update
        Returns:
            Response: JSON response with updated user data if successful,
                     or validation errors with 400 status if data is invalid
        Raises:
            Http404: If user with given pk does not exist
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Delete a user instance.

        Args:
            request: The HTTP request object.
            pk: Primary key of the user to be deleted.
        Returns:
            Response: HTTP 204 No Content response indicating successful deletion.
        Raises:
            Http404: If the user with the given primary key does not exist.
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, pk=None):
        """
        Retrieve user(s) information.
        
        If pk is provided, retrieves a specific user by their primary key.
        If pk is not provided, retrieves all users in the system.
        
        Args:
            request: HTTP request object
            pk (int, optional): Primary key of the user to retrieve. 
                               If None, all users are returned.
        Returns:
            Response: JSON response containing either:
                - Single user data if pk is provided
                - List of all users if pk is not provided
        Raises:
            Http404: If user with given pk does not exist
        """
        if pk:
            user = self.get_object(pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

