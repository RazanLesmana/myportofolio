from django.forms import ModelForm
from main.models import Project
from django.forms import ModelForm
from main.models import Project, Experience
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

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

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "company",
            "company_logo",
            "company_order",
            "title",
            "description",
            "category",
            "period",
            "ended_at",
            "is_featured",
            "order",
        ]
        labels = {
            "company": "Nama Perusahaan/Organisasi",
            "company_logo": "Path Logo",
            "company_order": "Urutan Perusahaan",
            "title": "Jabatan/Posisi",
            "description": "Deskripsi",
            "category": "Kategori",
            "period": "Periode",
            "ended_at": "Tanggal Selesai",
            "is_featured": "Tampilkan di halaman utama",
            "order": "Urutan Jabatan",
        }