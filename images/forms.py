# images/forms.py
from django import forms
from .models import BaseImage, BusinessImage

class BaseImageForm(forms.ModelForm):
    class Meta:
        model = BaseImage
        fields = ['name', 'version', 'image_id', 'size', 'status', 'category', 'description']

#
# class BusinessImageForm(forms.ModelForm):
#     class Meta:
#         model = BusinessImage
#         # 如果你的模型字段还是 project_id，就把 'project' 改为 'project_id'
#         fields = ['name', 'version', 'image_file', 'image_id', 'project', 'detect_status', 'approve_status', 'size']
#
#
# class BusinessImageForm(forms.ModelForm):
#     # 新增：文件上传字段（放在前面，渲染时更直观）
#     image_file = forms.FileField(
#         required=True,
#         label="镜像文件",
#         widget=forms.ClearableFileInput(attrs={
#             "class": "form-control",
#             "accept": ".tar,.tar.gz,.tgz,.img,.zip,.gz",  # 可按需调整
#             "style": "border: 1px solid #ddd; padding: 5px;"
#         })
#     )
#
#     class Meta:
#         model = BusinessImage
#         # 保留你原来的字段 + 新增 image_file
#         fields = ['name', 'version', 'image_file', 'image_id', 'project', 'detect_status', 'approve_status', 'size']
#
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': '请输入镜像名称',
#                 'style': 'border: 1px solid #ddd; padding: 5px;'
#             }),
#             'version': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': '请输入镜像版本',
#                 'style': 'border: 1px solid #ddd; padding: 5px;'
#             }),
#             'image_id': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': '镜像ID（可自动生成）',
#                 'style': 'border: 1px solid #ddd; padding: 5px;',
#                 'readonly': 'readonly'  # 假设该字段自动生成，不需要用户输入
#             }),
#             'project': forms.Select(attrs={
#                 'class': 'form-select',
#                 'style': 'border: 1px solid #ddd; padding: 5px;'
#             }),
#             'detect_status': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'style': 'border: 1px solid #ddd; padding: 5px;',
#                 'readonly': 'readonly'  # 可设置为只读，如果你希望用户不能修改它
#             }),
#             'approve_status': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'style': 'border: 1px solid #ddd; padding: 5px;',
#                 'readonly': 'readonly'  # 可设置为只读，如果你希望用户不能修改它
#             }),
#             'size': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': '自动生成，用户不可修改',
#                 'readonly': 'readonly',
#                 'style': 'border: 1px solid #ddd; padding: 5px;'
#             })
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # 这三个字段通常不让用户手填（避免必填报错）
#         self.fields['image_id'].required = False
#         self.fields['detect_status'].required = False
#         self.fields['approve_status'].required = False
#         self.fields['size'].required = False
#         # 给默认值，避免校验不通过
#         self.fields['detect_status'].initial = self.fields['detect_status'].initial or '待检测'
#         self.fields['approve_status'].initial = self.fields['approve_status'].initial or '无需'
#
#     def clean(self):
#         """如果用户没填 size / image_id，这里用文件自动补上"""
#         cleaned = super().clean()
#         f = cleaned.get('image_file')
#         if f:
#             # 用文件大小（字节）回填数据库的 size（你也可以换成 MB，注意字段类型）
#             cleaned['size'] = f.size
#             # 如果没填写 image_id，就自动给一个（也可以在视图里做）
#             if not cleaned.get('image_id'):
#                 import hashlib
#                 hasher = hashlib.sha256()
#                 for chunk in f.chunks():
#                     hasher.update(chunk)
#                 cleaned['image_id'] = hasher.hexdigest()[:32]
#         return cleaned


class BusinessImageForm(forms.ModelForm):
    # 新增：文件上传字段（放在前面，渲染时更直观）
    image_file = forms.FileField(
        required=True,
        label="镜像文件",
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
            "accept": ".tar,.tar.gz,.tgz,.img,.zip,.gz",  # 可按需调整
            "style": "border: 1px solid #ddd; padding: 5px;"
        })
    )

    class Meta:
        model = BusinessImage
        # 保留你原来的字段 + 新增 image_file
        fields = ['name', 'version', 'image_file', 'image_id', 'project', 'detect_status', 'approve_status', 'size']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入镜像名称',
                'style': 'border: 1px solid #ddd; padding: 10px; font-size: 14px;'
            }),
            'version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入镜像版本',
                'style': 'border: 1px solid #ddd; padding: 10px; font-size: 14px;'
            }),
            'image_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '镜像ID（可自动生成）',
                'style': 'border: 1px solid #ddd; padding: 10px; font-size: 14px;',
                'readonly': 'readonly'  # 假设该字段自动生成，不需要用户输入
            }),
            'project': forms.Select(attrs={
                'class': 'form-select',
                'style': 'border: 1px solid #ddd; padding: 10px; font-size: 14px;'
            }),
            'detect_status': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid #ddd; padding: 10px; font-size: 14px;',
                'readonly': 'readonly'  # 可设置为只读，如果你希望用户不能修改它
            }),
            'approve_status': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid #ddd; padding: 10px; font-size: 14px;',
                'readonly': 'readonly'  # 可设置为只读，如果你希望用户不能修改它
            }),
            'size': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '自动生成，用户不可修改',
                'readonly': 'readonly',
                'style': 'border: 1px solid #ddd; padding: 10px; font-size: 14px;'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 这三个字段通常不让用户手填（避免必填报错）
        self.fields['image_id'].required = False
        self.fields['detect_status'].required = False
        self.fields['approve_status'].required = False
        self.fields['size'].required = False
        # 给默认值，避免校验不通过
        self.fields['detect_status'].initial = self.fields['detect_status'].initial or '待检测'
        self.fields['approve_status'].initial = self.fields['approve_status'].initial or '无需'

    def clean(self):
        """如果用户没填 size / image_id，这里用文件自动补上"""
        cleaned = super().clean()
        f = cleaned.get('image_file')
        if f:
            # 用文件大小（字节）回填数据库的 size（你也可以换成 MB，注意字段类型）
            cleaned['size'] = f.size
            # 如果没填写 image_id，就自动给一个（也可以在视图里做）
            if not cleaned.get('image_id'):
                import hashlib
                hasher = hashlib.sha256()
                for chunk in f.chunks():
                    hasher.update(chunk)
                cleaned['image_id'] = hasher.hexdigest()[:32]
        return cleaned