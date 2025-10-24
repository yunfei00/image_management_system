# apps/detects/forms.py
from django import forms

from detection.models import DetectTool, ProjectDetectTool, PreDetectRecord, SecurityDetectApply, DetectCenterConfig, \
    DetectDevice


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


class DetectApplyForm(forms.ModelForm):
    class Meta:
        model = SecurityDetectApply
        fields = ['project', 'file_paths', 'detect_items', 'description', 'assign_team', 'status']


class DetectCenterConfigForm(forms.ModelForm):
    # Django5 原生 JSONField 表单，自动校验 JSON
    api_config = forms.JSONField(label="API配置", required=True)
    device_config = forms.JSONField(label="设备配置", required=False)

    class Meta:
        model = DetectCenterConfig
        fields = ['name', 'api_config', 'approval_flow', 'device_config', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '配置名称'}),
            'approval_flow': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class DetectDeviceForm(forms.ModelForm):
    config = forms.JSONField(label="设备配置", required=False)

    class Meta:
        model = DetectDevice
        fields = ['name', 'type', 'api_url', 'config', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '设备名称，如：绿盟'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '类型，如：NSFOCUS/小佑/默安'}),
            'api_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_api_url(self):
        # 如果想做附加校验可加在这里
        return self.cleaned_data.get('api_url')
