from django import forms

from detection.models import DetectTool
from .models import Department, User, Role, LoginLog, OperationLog, Menu, Position, Permission, ApprovalFlow


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

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

User = get_user_model()

class UserForm(forms.ModelForm):
    # 默认先设为非必填，新增时在 __init__ 里再设为必填
    password = forms.CharField(
        label='密码',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码', 'class': 'form-control'}),
        help_text='新增用户必填，保存时自动加密'
    )
    confirm_password = forms.CharField(
        label='确认密码',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': '请确认密码', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'role', 'department', 'status', 'password']
        labels = {
            'username': '用户名',
            'phone': '手机号',
            'email': '邮箱',
            'role': '角色',
            'department': '部门',
            'status': '状态',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入手机号'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}),
            # 若 role / department 是外键，使用 Select；若多选则用 SelectMultiple
            'role': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            # status 若是布尔：CheckboxInput；若是枚举：Select
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        """
        新增：显示并要求密码与确认密码；编辑：移除两项（不显示）
        """
        super().__init__(*args, **kwargs)
        is_edit = bool(self.instance and self.instance.pk)
        if is_edit:
            # 编辑模式：不显示密码相关字段
            self.fields.pop('password', None)
            self.fields.pop('confirm_password', None)
        else:
            # 新增模式：密码必填并校验
            self.fields['password'].required = True
            self.fields['confirm_password'].required = True

    def clean(self):
        cleaned_data = super().clean()
        # 只有在“新增/显示了密码字段”时才进行密码校验
        if 'password' in self.fields:
            pwd = cleaned_data.get('password')
            cpwd = cleaned_data.get('confirm_password')

            # 一致性校验
            if pwd and cpwd and pwd != cpwd:
                self.add_error('confirm_password', '两次输入的密码不一致')

            # 强度校验（使用 Django 内置校验器，需在 settings 配置 AUTH_PASSWORD_VALIDATORS）
            if pwd:
                try:
                    password_validation.validate_password(pwd, user=self.instance)
                except forms.ValidationError as e:
                    # 将多条校验信息合并到 password 字段
                    self.add_error('password', e)
        return cleaned_data

    def save(self, commit=True):
        """
        新增：set_password 后保存；
        编辑：不触碰密码，仅保存其他字段。
        """
        user = super().save(commit=False)
        # 只有当表单里含有 password 字段并且用户填写了密码时才加密设置
        if 'password' in self.cleaned_data and self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            self.save_m2m()
        return user


class AdminResetPasswordForm(forms.Form):
    """
    管理员为指定用户重置密码（无需旧密码）
    """
    new_password = forms.CharField(
        label='新密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入新密码'}),
    )
    confirm_password = forms.CharField(
        label='确认新密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入新密码'}),
    )

    def __init__(self, *args, **kwargs):
        # 传入要重置的用户（用于强度校验器）
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get('new_password')
        cpwd = cleaned.get('confirm_password')

        if pwd and cpwd and pwd != cpwd:
            self.add_error('confirm_password', '两次输入的密码不一致')

        if pwd:
            try:
                password_validation.validate_password(pwd, user=self.user)
            except forms.ValidationError as e:
                self.add_error('new_password', e)
        return cleaned

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


class ApprovalFlowForm(forms.ModelForm):
    # Django 5 自带 JSONField 表单字段，可自动校验 JSON
    nodes_config = forms.JSONField(label="审批节点配置")

    class Meta:
        model = ApprovalFlow
        fields = ["name", "nodes_config", "status"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入流程名称"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }