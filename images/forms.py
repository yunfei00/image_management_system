# images/forms.py
import hashlib

from django import forms
from .models import BaseImage, BusinessImage

class BaseImageForm(forms.ModelForm):
    class Meta:
        model = BaseImage
        fields = ['name', 'version', 'image_file', 'image_id', 'size', 'status', 'category', 'description']
        exclude = ['size']  # 或者 fields = [... 不含 size ...]


# class BusinessImageForm(forms.ModelForm):
#     class Meta:
#         model = BusinessImage
#         # 如果你的模型字段还是 project_id，就把 'project' 改为 'project_id'
#         fields = ['name', 'version', 'image_file', 'image_id', 'project', 'detect_status', 'approve_status', 'size']


class BusinessImageForm(forms.ModelForm):
    # 文件上传字段（名字必须叫 image_file，和模型字段一致）
    image_file = forms.FileField(
        label="镜像文件",
        required=True,  # 需要用户必须上传
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
            "accept": ".tar,.tar.gz,.tgz,.img,.zip,.gz"  # 按需调整
        })
    )

    class Meta:
        model = BusinessImage
        # 建议把“用户可编辑的字段”排前面，系统生成的放后面
        fields = [
            "project", "name", "version",
            "image_file",              # ← 必须和模板中的 name 匹配
            "image_id", "detect_status", "approve_status", "size"
        ]
        labels = {
            "project": "所属项目",
            "name": "镜像名称",
            "version": "版本",
            "image_id": "镜像ID",
            "detect_status": "检测状态",
            "approve_status": "审批状态",
            "size": "大小（字节）",
        }
        widgets = {
            "project": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "仓库/镜像名"}),
            "version": forms.TextInput(attrs={"class": "form-control", "placeholder": "例如 1.0.0"}),
            # 下三项通常由后端生成/回填，表单里只读展示
            "image_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "自动生成", "readonly": True}),
            "detect_status": forms.TextInput(attrs={"class": "form-control", "placeholder": "自动填充：待检测", "readonly": True}),
            "approve_status": forms.TextInput(attrs={"class": "form-control", "placeholder": "自动填充：无需", "readonly": True}),
            "size": forms.NumberInput(attrs={"class": "form-control", "placeholder": "自动回填（字节）", "readonly": True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 这三个给默认值且不强制
        self.fields["image_id"].required = False
        self.fields["detect_status"].required = False
        self.fields["approve_status"].required = False
        self.fields["size"].required = False

        if not self.initial.get("detect_status"):
            self.initial["detect_status"] = "待检测"
        if not self.initial.get("approve_status"):
            self.initial["approve_status"] = "无需"

    # 单字段校验：格式/大小限制
    def clean_image_file(self):
        f = self.cleaned_data.get("image_file")
        if not f:
            return f
        # 大小限制（例：5GB）
        if f.size > 5 * 1024 * 1024 * 1024:
            raise forms.ValidationError("文件过大（>5GB）。")
        # 简单后缀校验
        allowed = (".tar", ".tar.gz", ".tgz", ".img", ".zip", ".gz")
        name = f.name.lower()
        if not any(name.endswith(ext) for ext in allowed):
            raise forms.ValidationError("仅支持文件类型：" + ", ".join(allowed))
        return f

    # 表单总校验：自动生成 image_id / 回填 size，并把文件指针回卷
    def clean(self):
        cleaned = super().clean()
        f = cleaned.get("image_file")
        if f:
            # 读取计算 hash 会把文件指针推到末尾，必须回卷！
            hasher = hashlib.sha256()
            for chunk in f.chunks():
                hasher.update(chunk)
            if not cleaned.get("image_id"):
                cleaned["image_id"] = hasher.hexdigest()[:32]
            cleaned["size"] = f.size
            try:
                f.seek(0)  # ← 关键：回到文件开头，避免保存成空文件
            except Exception:
                pass
        # 默认状态兜底
        cleaned["detect_status"] = cleaned.get("detect_status") or "待检测"
        cleaned["approve_status"] = cleaned.get("approve_status") or "无需"
        return cleaned