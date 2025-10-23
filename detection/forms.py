# apps/detects/forms.py
from django import forms

from detection.models import DetectTool, ProjectDetectTool, PreDetectRecord


class DetectToolForm(forms.ModelForm):
    class Meta:
        model = DetectTool
        fields = ['name', 'type', 'api_url', 'config', 'status']
        # 可选：让 JSON 在表单里更好编辑（保留简洁风格，不需要可删）
        widgets = {
            'config': forms.Textarea(attrs={'rows': 6, 'class': 'form-control font-monospace'}),
        }


class ProjectDetectToolForm(forms.ModelForm):
    class Meta:
        model = ProjectDetectTool
        fields = ['project', 'tool', 'config', 'available']
        widgets = {
            'config': forms.Textarea(attrs={'rows': 6, 'class': 'form-control font-monospace'}),
        }


class PreDetectRecordForm(forms.ModelForm):
    class Meta:
        model = PreDetectRecord
        # demo 下由系统自动置状态/时间，这里仅保留创建必要字段
        fields = ['project', 'tool', 'payload', 'request_id']
        widgets = {
            'payload': forms.Textarea(attrs={'rows': 6, 'class': 'form-control font-monospace'}),
        }
