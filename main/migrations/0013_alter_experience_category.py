
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_experience_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='category',
            field=models.CharField(choices=[('internship', 'Internship'), ('organization', 'Organization'), ('committee', 'Committee'), ('volunteer', 'Volunteer')], default='volunteer', max_length=20),
        ),
    ]
