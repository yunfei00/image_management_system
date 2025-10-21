from django import forms
from .models import Department, User, Role, LoginLog, OperationLog, Menu, Position

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
        fields = ['username', 'email']
        # fields = ['username', 'phone', 'email', 'role', 'department', 'status']
#
# class DictForm(forms.ModelForm):
#     class Meta:
#         model = DictItem
#         fields = ['name', 'type', 'value', 'status']
#
#
# class ToolForm(forms.ModelForm):
#     class Meta:
#         model = DetectTool
#         fields = ['name', 'type', 'api_url', 'config', 'status']


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