from django.shortcuts import render

from main.models import Experience, OutsidePhoto, Project

def show_main(request):
    context = {
        "name": "Razan Lesmana",
        "npm": "2506604656",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Bridging problem and real solution through tech, exploring business & consulting, a leader at heart."
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
        "hero_photo": OutsidePhoto.objects.filter(is_hero=True).first(), #first biar ga index error
        "photography_photos": OutsidePhoto.objects.filter(section="photography", is_hero=False),
        "travel_photos": OutsidePhoto.objects.filter(section="travel", is_hero=False),
        "runs_photos": OutsidePhoto.objects.filter(section="runs", is_hero=False),
    }
    return render(request, "outside_work.html", context)