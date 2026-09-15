from django.forms import ModelForm
from main.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "project_type",
            "image_path",
            "link",
            "link_label",
            "link_2",
            "link_2_label",
            "is_featured",
        ]