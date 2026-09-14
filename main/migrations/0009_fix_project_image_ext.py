from django.db import migrations


def jpg_to_png(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    for p in Project.objects.all():
        if p.image_path.endswith(".jpg"):
            p.image_path = p.image_path[:-4] + ".png"
            p.save()


def png_to_jpg(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    for p in Project.objects.all():
        if p.image_path.endswith(".png"):
            p.image_path = p.image_path[:-4] + ".jpg"
            p.save()


class Migration(migrations.Migration):

    dependencies = [
            ('main', '0008_seed_projects'),
        ]
    
    operations = [
        migrations.RunPython(jpg_to_png, png_to_jpg),
    ]
