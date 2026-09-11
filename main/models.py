import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
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