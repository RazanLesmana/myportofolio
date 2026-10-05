from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers

from main.models import Experience, OutsidePhoto, Project
from main.forms import ExperienceForm, ProjectForm
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

import datetime

from django.contrib.auth.decorators import login_required  # Tambahkan baris ini
from django.core.exceptions import PermissionDenied        # Tambahkan baris ini
from django.views.decorators.http import require_POST

from django.http import JsonResponse
from main.forms import ProjectForm
from django.templatetags.static import static
from django.views.decorators.http import require_POST

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
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
        "last_login": last_login,
    }
    return render(request, "index.html", context)

def user_is_editor(user):
    return user.groups.filter(name="Editor").exists()

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
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Razan Lesmana",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, "Project berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {"form": form, "name": "Razan Lesmana"}
    return render(request, "project_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "project_type": project.project_type,
                "project_type_display": project.get_project_type_display(),
                "image_url": static(project.image_path) if project.image_path else "",
                "link": project.link,
                "link_label": project.link_label,
                "link_2": project.link_2,
                "link_2_label": project.link_2_label,
                "is_featured": project.is_featured,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
            raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

# ===== EXPERIENCE =====
def show_experiences(request):
    title_query = request.GET.get("title", "").strip()
    context = {
        "name": "Razan Lesmana",
        "title_query": title_query,
        "is_editor": request.user.is_authenticated and user_is_editor(request.user),
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related("stars").all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for experience in experiences:
        starred_users = experience.stars.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "company": experience.company,
                "description": experience.description,
                "category": experience.get_category_display(),      
                "period": experience.period,
                "is_ongoing": experience.is_ongoing,                  
                "star_count": starred_users.count(),                 
                "is_starred": is_starred,                            
                "starred_by_names": ", ".join(u.username for u in starred_users),
            }
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, "Experience berhasil ditambahkan!")
        return redirect("main:show_experiences")

    context = {
        "form": form,
        "name": "Razan Lesmana",
        "form_title": "Tambah Experience",
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    if not (request.user.is_superuser or user_is_editor(request.user)):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, "Experience berhasil diubah!")
        return redirect("main:show_experiences")

    context = {
        "form": form,
        "name": "Razan Lesmana",
        "form_title": "Edit Experience",
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experiences")

    return redirect("main:show_experiences")


@login_required(login_url="/login/")
@require_POST
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if experience.stars.filter(pk=request.user.pk).exists():
        experience.stars.remove(request.user)
    else:
        experience.stars.add(request.user)

    return redirect("main:show_experiences")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Razan Lesmana",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response 

    context = {
        "name": "Razan Lesmana",
        "form": form,
    }

    return render(request, "login.html", context)

def user_logout(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return redirect("main:show_main")

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan experience."},
            status=403,
        )
    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)