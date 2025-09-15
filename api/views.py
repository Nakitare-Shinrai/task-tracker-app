from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Client, UserRoleType, Branch, CustomUser, Task
from .serializers import ClientSerializer, UserRoleTypeSerializer, BranchSerializer, UserSerializer, TaskSerializer

# Create your views here.
class clientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

class userRoleTypeViewSet(viewsets.ModelViewSet):
    queryset = UserRoleType.objects.all()
    serializer_class = UserRoleTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class branchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Branch.objects.all()
        client_id = self.request.query_params.get('client_id')
        if client_id:
            queryset = queryset.filter(client__id=client_id)
        return queryset
    
class userViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        role_id = self.request.query_params.get('role_id')
        branch_id = self.request.query_params.get('branch_id')
        
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        
        return queryset
    
class taskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.all()
        user_id = self.request.query_params.get('user_id')
        assignee_id = self.request.query_params.get('assignee_id')
        status = self.request.query_params.get('status')

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if assignee_id:
            queryset = queryset.filter(assignee_id=assignee_id)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset