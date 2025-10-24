from report.models import Report
from django import forms

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['type', 'data', 'period', 'project_status', 'department']

    # 添加任何字段的额外验证或自定义逻辑
    def clean_data(self):
        data = self.cleaned_data.get('data')
        if not data:
            raise forms.ValidationError('报表数据不能为空')
        return data