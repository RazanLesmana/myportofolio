import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('organization', 'Organization'),
        ('committee', 'Committee')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    company = models.CharField(max_length=255, blank=True)
    company_logo = models.CharField(max_length=255, blank=True)
    company_order = models.PositiveIntegerField(default=0)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='volunteer')
    period = models.CharField(max_length=100, blank=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['company_order', 'order']

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

class OutsidePhoto(models.Model):
    SECTION_CHOICES = [
        ('photography', 'Photography'),
        ('travel', 'Travel'),
        ('runs', 'Runs'),
    ]

    id = id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='photography')
    album = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    caption = models.TextField(blank=True)
    taken_at = models.DateField(blank=True, null=True)
    is_hero = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['section', 'album', 'order']

    def __str__(self):
        return f"{self.album} - {self.title}"
    