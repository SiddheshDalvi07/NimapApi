from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectListSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='name')
    client_name = serializers.CharField(source='client.name', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name', 'created_at', 'created_by']

class ProjectDetailSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='name')
    client = serializers.CharField(source='client.name', read_only=True)
    users = UserSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']


class ProjectShortSerializer(serializers.ModelSerializer): 
    project_name = serializers.CharField(source='name')
    class Meta:
        model = Project
        fields = ['id', 'project_name']


class ClientListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='name')
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']


class ClientDetailSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='name')
    projects = ProjectShortSerializer(many=True, read_only=True)
    created_by = serializers.CharField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']



