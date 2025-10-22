from django import forms

from detection.models import DetectTool
from .models import Department, User, Role, LoginLog, OperationLog, Menu, Position, Permission


class DeptForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'leader', 'status']

class RoleForm(forms.ModelForm):
    # 自定义permissions字段：使用checkbox多选，显示Permission的name
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),  # 可选的权限列表
        widget=forms.CheckboxSelectMultiple(attrs={"class": "permission-checkboxes"}),  # 核心：使用checkbox控件
        label="权限"
    )
    class Meta:
        model = Role
        fields = ['name', 'code', 'permissions', 'status']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        # fields = ['username', 'phone', 'email', 'role', 'department', 'status']

class ToolForm(forms.ModelForm):
    class Meta:
        model = DetectTool
        fields = ['name', 'type', 'api_url', 'config', 'status']


# class MenuForm(forms.ModelForm):
#     class Meta:
#         model = Menu
#         fields = ['name', 'path', 'parent', 'status']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'parent', 'path', 'icon', 'sort',
                  'status', 'visible', 'is_external', 'permission', 'groups']
        widgets = {
            'groups': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned = super().clean()
        path = cleaned.get('path') or ''
        is_external = cleaned.get('is_external')
        if not is_external and not path.startswith('/'):
            raise forms.ValidationError('非外链路径必须以 “/” 开头。')
        return cleaned

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

class LoginLogForm(forms.ModelForm):
    class Meta:
        model = LoginLog
        fields = ['username', 'ip', 'status', 'result']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
            'ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '登录IP'}),
            'status': forms.Select(choices=[(True, '成功'), (False, '失败')], attrs={'class': 'form-select'}),
            'result': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '登录结果描述'}),
        }

class LoginLogSearchForm(forms.Form):
    username = forms.CharField(required=False, label="用户名")
    ip = forms.CharField(required=False, label="登录IP")
    status = forms.ChoiceField(
        choices=[('', '全部'), ('true', '成功'), ('false', '失败')],
        required=False,
        label="状态"
    )
    start_time = forms.DateTimeField(required=False, label="开始时间", widget=forms.DateInput(attrs={'type': 'date'}))
    end_time = forms.DateTimeField(required=False, label="结束时间", widget=forms.DateInput(attrs={'type': 'date'}))

class OperationLogSearchForm(forms.Form):
    start_time = forms.DateTimeField(required=False, label="开始时间", widget=forms.DateInput(attrs={'type': 'date'}))
    end_time = forms.DateTimeField(required=False, label="结束时间", widget=forms.DateInput(attrs={'type': 'date'}))
    module = forms.CharField(required=False, max_length=128, label="模块")
    operator = forms.CharField(required=False, max_length=64, label="操作员")
    ip = forms.CharField(required=False, max_length=45, label="登录IP")