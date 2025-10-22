from django import forms

from projects.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "code", "name", "applicant", "department", "end_user",
            "description", "plan_online_date", "base_image",
            "components", "status",
            "approval_status",
            # "approval_flow",
        ]