# images/forms.py
from django import forms
from .models import BaseImage, BusinessImage

class BaseImageForm(forms.ModelForm):
    class Meta:
        model = BaseImage
        fields = ['name', 'version', 'image_id', 'size', 'status', 'category', 'description']


class BusinessImageForm(forms.ModelForm):
    class Meta:
        model = BusinessImage
        # 如果你的模型字段还是 project_id，就把 'project' 改为 'project_id'
        fields = ['name', 'version', 'image_id', 'project', 'detect_status', 'approve_status', 'size']
