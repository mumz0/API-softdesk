from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', "password", 'date_of_birth', 'can_be_contacted', 'can_data_be_shared', "is_active", "is_staff", "is_superuser"]
        
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
