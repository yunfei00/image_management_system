from django import forms

from repo.models import Repository


class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ['name', 'type', 'images_json', 'environment_config']

    images_json = forms.JSONField(label="镜像信息", required=False)
    environment_config = forms.JSONField(label="环境配置", required=False)
