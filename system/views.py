from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import (Permission, Role, RoleUser, Department, Position, DetectTool,
                     LoginLog, OperationLog, Menu, ApprovalFlow)
from .serializers.user import (PermissionSerializer, RoleSerializer, RoleUserSerializer, DepartmentSerializer,
                          PositionSerializer, DetectToolSerializer, LoginLogSerializer, OperationLogSerializer,
                          MenuSerializer, ApprovalFlowSerializer, UserSerializer)
from .utils import has_perm
import datetime
import requests
from django.core.mail import send_mail

User = get_user_model()

# Permissions/Role/RoleUser
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all().order_by('key')
    serializer_class = PermissionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['key','name']

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('-created_at')
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','code']
    def get_serializer_class(self):
        return RoleSerializer

class RoleUserViewSet(viewsets.ModelViewSet):
    queryset = RoleUser.objects.select_related('user','role').all().order_by('-assigned_at')
    serializer_class = RoleUserSerializer

    @action(detail=False, methods=['post'])
    def assign(self, request):
        user_id = request.data.get('user')
        role_id = request.data.get('role')
        if not user_id or not role_id:
            return Response({'detail':'user and role required'}, status=status.HTTP_400_BAD_REQUEST)
        obj, created = RoleUser.objects.get_or_create(user_id=user_id, role_id=role_id)
        return Response(RoleUserSerializer(obj).data)

# Departments
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('-created_at')
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','code']

    @action(detail=False, methods=['get'])
    def export(self, request):
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

# Positions
class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all().order_by('-created_at')
    serializer_class = PositionSerializer

# Detect Tools
class DetectToolViewSet(viewsets.ModelViewSet):
    queryset = DetectTool.objects.all().order_by('-created_at')
    serializer_class = DetectToolSerializer