from django.templatetags.static import static
from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Project


class PortfolioSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    star_relation = "starred_by"
    text_fields = ()

    def validate(self, attrs):
        for field in self.text_fields:
            if field in attrs:
                attrs[field] = strip_tags(attrs[field]).strip()
        if "title" in attrs and not attrs["title"]:
            raise serializers.ValidationError({"title": "Judul tidak boleh kosong atau hanya berisi tag HTML."})
        return attrs

    def get_star_count(self, obj):
        return getattr(obj, self.star_relation).count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated
                    and request.user in getattr(obj, self.star_relation).all())

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in getattr(obj, self.star_relation).all())


class ProjectSerializer(PortfolioSerializer):
    project_type_display = serializers.CharField(source="get_project_type_display", read_only=True)
    image_url = serializers.SerializerMethodField()
    text_fields = ("title", "description", "link_label", "link_2_label")

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "project_type", "project_type_display",
            "image_path", "image_url", "link", "link_label", "link_2", "link_2_label",
            "is_featured", "order", "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def get_image_url(self, obj):
        return static(obj.image_path) if obj.image_path else ""


class ExperienceSerializer(PortfolioSerializer):
    star_relation = "stars"
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    text_fields = ("title", "company", "description", "period", "ended_at")

    class Meta:
        model = Experience
        fields = [
            "id", "company", "company_logo", "company_order", "title", "description",
            "category", "category_display", "period", "ended_at", "is_ongoing",
            "is_featured", "order", "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]
