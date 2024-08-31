from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets, permissions, status 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.exceptions import ValidationError
# Create your views here.


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classses = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClientListSerializer
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientListSerializer

    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)
        
    def perform_update(self,serializer):
        serializer.save()


    # @action(detail=True,methods=['get'])
    # def projects(self, request, pk=None):
    #     client = self.get_object()
    #     projects = client.projects.all()
    #     serializer = ProjectSerializer(projects, many=True)
    #     return Response(serializer.data)
    

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        loggedin = Project.objects.filter(users=user)
        return loggedin


    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectDetailSerializer
    
    

    def perform_create(self, serializer):
        try:
            client_id = self.request.data.get('client_id')
            client = Client.objects.get(id=client_id)
            users = self.request.data.get('users', [])
            user_instances = User.objects.filter(id__in=users)
            project = serializer.save(created_by=self.request.user, client=client)
            project.users.set(user_instances)
        except Exception as e:
            raise ValidationError({"detail": "A project with this name already exists for another client."})

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=False, methods=['get'])
    def my_projects(self, request):
        user = request.user
        projects = user.assigned_projects.all()
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('api/')  
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')