from django.urls import path
from main.views import (
    show_main,
    show_experience,
    show_outside_work,
    show_projects,
    create_project,
    get_projects_json,
    delete_project,
    show_xml,
    show_json,
    show_xml_by_id,
    show_json_by_id,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("outside-work/", show_outside_work, name="show_outside_work"),
        path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path("xml/<str:project_id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<str:project_id>/", show_json_by_id, name="show_json_by_id"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
]