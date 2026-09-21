from django.urls import path
from main.views import (
    show_main,
    show_outside_work,
    show_projects,
    create_project,
    get_projects_json,
    delete_project,
    show_experiences,
    create_experience,
    get_experiences_json,
    delete_experience,

)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("outside-work/", show_outside_work, name="show_outside_work"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("experiences/", show_experiences, name="show_experiences"),
    path("experiences/add/", create_experience, name="create_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("experiences/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
]