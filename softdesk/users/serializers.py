from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    This serializer handles the serialization and deserialization of CustomUser instances,
    exposing essential user fields while protecting sensitive administrative fields.

    Fields:
        - id: User's unique identifier (read-only)
        - username: User's unique username
        - password: User's password (write-only in practice)
        - date_of_birth: User's date of birth
        - can_be_contacted: Boolean indicating if user can be contacted
        - can_data_be_shared: Boolean indicating if user's data can be shared
        - is_active: Boolean indicating if user account is active (read-only)
        - is_staff: Boolean indicating if user has staff privileges (read-only)
        - is_superuser: Boolean indicating if user has superuser privileges (read-only)

    Note:
        Administrative fields (is_active, is_staff, is_superuser) and the user ID
        are read-only to prevent unauthorized privilege escalation and maintain
        data integrity.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', "password", 'date_of_birth', 'can_be_contacted', 'can_data_be_shared', "is_active", "is_staff", "is_superuser"]
        read_only_fields = ["id", "is_superuser", "is_staff", "is_active"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user