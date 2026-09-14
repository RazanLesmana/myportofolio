from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, OutsidePhoto


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    class OutsideWorkTest(TestCase):
        def setUp(self):
            OutsidePhoto.objects.all().delete()

            self.photo = OutsidePhoto.objects.create(
                title="Marina Bay at Blue Hour",
                section="photography",
                album="Singapore, 2024",
                image_path="img/outside/singapore-01.jpg",
                order=1,
            )

        def test_outside_work_url_is_accessible(self):
            response = self.client.get(reverse("main:show_outside_work"))

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "outside_work.html")

        def test_outside_work_shows_model_data(self):
            response = self.client.get(reverse("main:show_outside_work"))

            self.assertContains(response, self.photo.title)
            self.assertContains(response, self.photo.album)
            self.assertContains(response, self.photo.image_path)

        def test_outside_work_empty_state(self):
            OutsidePhoto.objects.all().delete()
            response = self.client.get(reverse("main:show_outside_work"))

            self.assertContains(response, "Photos coming soon!")

        def test_travel_and_runs_show_coming_soon(self):
            response = self.client.get(reverse("main:show_outside_work"))

            self.assertContains(response, "Travel coming soon!")
            self.assertContains(response, "Coming soon.")

        def test_navbar_links_to_outside_work(self):
            response = self.client.get(reverse("main:show_main"))

            self.assertContains(response, f'href="{reverse("main:show_outside_work")}"')

        def test_outside_photo_str(self):
            self.assertEqual(str(self.photo), "Singapore, 2024 — Marina Bay at Blue Hour")
            