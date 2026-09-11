import uuid
from django.db import migrations


def seed_photos(apps, schema_editor):
    OutsidePhoto = apps.get_model("main", "OutsidePhoto")

    OutsidePhoto.objects.create(
        id=uuid.uuid4(),
        title="Foto Hero",
        section="photography",
        album="",
        image_path="img/outside/hero.jpg",
        is_hero=True,
        order=0,
    )

    for i in range(1, 10):
        OutsidePhoto.objects.create(
            id=uuid.uuid4(),
            title=f"Singapore {i}",
            section="photography",
            album="Singapore, 2024",
            image_path=f"img/outside/singapore-{i:02d}.jpg",
            order=i,
        )


def unseed_photos(apps, schema_editor):
    OutsidePhoto = apps.get_model("main", "OutsidePhoto")
    OutsidePhoto.objects.filter(image_path__startswith="img/outside/").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_outsidephoto')
    ]

    operations = [
        migrations.RunPython(seed_photos, unseed_photos),
    ]