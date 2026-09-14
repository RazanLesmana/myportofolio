import uuid
from django.db import migrations


def seed_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")

    rows = [
        dict(
            title="Mandiri ONE Strategy",
            project_type="case-competition",
            description="A prototype for our proposed solution at the IOC Case Competition final stage.",
            image_path="img/projects/one-strategy-preview.jpg",
            link="https://bats-lasso-15715503.figma.site/",
            link_label="Prototype link",
            link_2="", link_2_label="Final deck link",
            is_featured=True, order=1,
        ),
        dict(
            title="GoPlan",
            project_type="case-competition",
            description="A prototype for our proposed solution at the Gojek Mini Case Competition.",
            image_path="img/projects/goplan-preview.jpg",
            link="https://pear-stroke-72357914.figma.site/",
            link_label="Prototype link",
            link_2="", link_2_label="Final deck link",
            is_featured=True, order=2,
        ),
        dict(
            title="Sparks Compass Dashboard",
            project_type="case-competition",
            description="Helps Sparks English teachers and center managers monitor teaching quality.",
            image_path="img/projects/sparks-compass-preview.jpg",
            link="https://alert-payer-96678105.figma.site/",
            link_label="Prototype link",
            link_2="", link_2_label="",
            is_featured=True, order=3,
        ),
        dict(
            title="DDP0 About Page",
            project_type="coursework",
            description="The about page of the DDP0 2026 website.",
            image_path="img/projects/ddp0-about-preview.jpg",
            link="https://www.figma.com/proto/c8BSioHB9EO63hYfJ4HBz7/About?node-id=49-161&t=Q00zYXexBJt67sbo-1&starting-point-node-id=49%3A161",
            link_label="Website prototype link",
            link_2="", link_2_label="",
            is_featured=True, order=4,
        ),
    ]

    for r in rows:
        Project.objects.create(id=uuid.uuid4(), **r)


def unseed_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    Project.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_seed_experiences'),
    ]

    operations = [
        migrations.RunPython(seed_projects, unseed_projects),
    ]
