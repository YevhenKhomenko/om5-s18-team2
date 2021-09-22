from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'created_at', 'role', 'is_active',
                  'is_staff']


class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password',  'created_at', 'role', 'is_active',
                  'is_staff']
        read_only_fields = ['id', 'created_at', 'role', 'is_active',
                            'is_staff']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserDetailSerializer, self).create(validated_data)
