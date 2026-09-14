import datetime
from django.db import migrations


def dt(y, m):
    return datetime.datetime(y, m, 1, tzinfo=datetime.timezone.utc)


def seed_experiences(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")

    rows = [
        dict(
            company="Veritask", company_logo="img/veritask.jpg", company_order=1,
            title="[Pro-bono] External Consultant Analyst",
            period="Jul 2026 – Present",
            description="Collaborated as an external consultant under RISTEK's Special Project provision across 3 deliverables checkpoints.",
            category="volunteer", ended_at=None, is_featured=True, order=1,
        ),
        dict(
            company="RISTEK Fasilkom UI", company_logo="img/ristek.webp", company_order=2,
            title="Project Leader of RISTEK Hackathon 2026",
            period="Jul 2026 – Aug 2026",
            description="Lead coordination between RISTEK and Fasilkom UI's Division of Research and Innovation to launch RISTEK's first ever hackathon, gaining 40+ team participations with IDR 100 Mil+ Prize.",
            category="volunteer", ended_at=dt(2026, 8), is_featured=True, order=2,
        ),
        dict(
            company="RISTEK Fasilkom UI", company_logo="img/ristek.webp", company_order=2,
            title="Business Growth and Partnership Associate",
            period="Aug 2025 – Present",
            description="Worked with big companies: OpenAI, OpenClaw, etc. Achieved Best Member of Quarter 1 2025 and Most Outstanding SIG for Quarter 1 2025.",
            category="volunteer", ended_at=None, is_featured=True, order=3,
        ),
        dict(
            company="180 Degrees Consulting UI", company_logo="img/180dc.jpg", company_order=3,
            title="Competition Analyst of GBECC 2026",
            period="Jun 2026 – Present",
            description="Managing competition flow, specifically on judge's scoring.",
            category="volunteer", ended_at=None, is_featured=True, order=1,
        ),
        dict(
            company="OSIS SMA Negeri 5 Kota Bekasi", company_logo="img/sman5.jpg", company_order=4,
            title="Vice President",
            period="Feb 2023 – Feb 2024",
            description="Managed 89 student council members, delivering 30+ work programs.",
            category="volunteer", ended_at=dt(2024, 2), is_featured=True, order=1,
        ),
        dict(
            company="FESTIFIVE 2023", company_logo="img/Festifive.jpg", company_order=5,
            title="Project Officer",
            period="Feb 2023 – Sep 2023",
            description="Lead a team of 100+ students to execute the school's flagship program, gaining 2500+ participants across 36 competitions. Gaining event value of IDR 400 Million+",
            category="volunteer", ended_at=dt(2023, 9), is_featured=True, order=1,
        ),
    ]

    for r in rows:
        Experience.objects.create(**r)


def unseed_experiences(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")
    Experience.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_project_is_featured_project_link_2_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_experiences, unseed_experiences),
    ]