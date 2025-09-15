from rest_framework import serializers
from .models import Client, UserRoleType, Branch, CustomUser, Task
from django.contrib.auth.models import User

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class UserRoleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleType
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)

    class Meta:
        model = Branch
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    # password = serializers.CharField(source='user.password', write_only=True)
    # role = serializers.CharField(source='role.role', read_only=True)
    # branch = serializers.CharField(source='branch.location', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','username', 'email','password', 'first_name', 'last_name', 'role', 'branch', 'job_id', 'phone', 'date_created']

    extra_kwargs = {
        'branch': {'required': True},
        'role': {'required': True},
        'password': {'write_only': True, 'min_length': 8, 'required': True, 'style': {'input_type': 'password'}},
    }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)

        # This handles secure hashing of the password
        user.set_password(user_data['password'])
        user.save()

        custom_user = CustomUser.objects.create(user=user, **validated_data)
        return custom_user
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        # Update password if provided using secure hashing
        if 'password' in user_data:
            user.set_password(user_data.pop('password'))

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
class TaskSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.user.get_full_name', read_only=True)
    assignee_name = serializers.CharField(source='assignee.user.get_full_name', read_only=True)
    class Meta:
        model = Task
        fields = '__all__'
