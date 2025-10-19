from django import forms
from .models import Department, User, Role, DetectTool, LoginLog, OperationLog, Menu, Position, ApprovalFlow

class DeptForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'leader', 'status']

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'code', 'status']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'role', 'department', 'status']
#
# class DictForm(forms.ModelForm):
#     class Meta:
#         model = DictItem
#         fields = ['name', 'type', 'value', 'status']
#
#
class ToolForm(forms.ModelForm):
    class Meta:
        model = DetectTool
        fields = ['name', 'type', 'api_url', 'config', 'status']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'path', 'parent', 'status']


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'code', 'status']


# class WorkflowConfigForm(forms.ModelForm):
#     class Meta:
#         model = WorkflowConfig
#         fields = ['name', 'steps', 'status']
#         widgets = {'steps': forms.Textarea(attrs={'rows': 3})}
#
