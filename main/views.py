from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers

from main.models import Experience, OutsidePhoto, Project
from main.forms import ProjectForm
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404


def show_main(request):
    context = {
        "name": "Razan Lesmana",
        "npm": "2506604656",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Bridging problem and real solution through tech, "
            "exploring business & consulting, a leader at heart."
        ),
        "featured_experiences": Experience.objects.filter(is_featured=True),
        "featured_projects": Project.objects.filter(is_featured=True),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Razan Lesmana",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_outside_work(request):
    context = {
        "name": "Razan Lesmana",
        "hero_photo": OutsidePhoto.objects.filter(is_hero=True).first(),
        "photography_photos": OutsidePhoto.objects.filter(section="photography", is_hero=False),
        "travel_photos": OutsidePhoto.objects.filter(section="travel", is_hero=False),
        "runs_photos": OutsidePhoto.objects.filter(section="runs", is_hero=False),
    }
    return render(request, "outside_work.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Razan Lesmana",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)


def create_project(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, "Project berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {"form": form, "name": "Razan Lesmana"}
    return render(request, "project_form.html", context)


def show_xml(request):
    project_list = Project.objects.all()
    xml_data = serializers.serialize("xml", project_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    project_list = Project.objects.all()
    json_data = serializers.serialize("json", project_list)
    return HttpResponse(json_data, content_type="application/json")


def show_xml_by_id(request, project_id):
    try:
        project_item = Project.objects.filter(pk=project_id)
        xml_data = serializers.serialize("xml", project_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Project.DoesNotExist:
        return HttpResponse(status=404)


def show_json_by_id(request, project_id):
    try:
        project_item = Project.objects.get(pk=project_id)
        json_data = serializers.serialize("json", [project_item])
        return HttpResponse(json_data, content_type="application/json")
    except Project.DoesNotExist:
        return HttpResponse(status=404)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")