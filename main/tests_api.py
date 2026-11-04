import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Project
from main.serializers import ProjectSerializer


class ProjectAPITest(APITestCase):
    def setUp(self):
        # Data migrations seed real portfolio content; isolate this API fixture.
        Project.objects.all().delete()
        self.owner = User.objects.create_superuser('owner', 'owner@example.com', 'test-password')
        self.visitor = User.objects.create_user('visitor', password='test-password')
        self.project = Project.objects.create(title='Portfolio', description='My website')
        self.list_url = reverse('api:project-list')
        self.detail_url = reverse('api:project-detail', args=[self.project.pk])
        self.star_url = reverse('api:project-star', args=[self.project.pk])
        self.payload = {'title': 'New project', 'description': 'A useful app',
                        'project_type': 'personal', 'link': 'https://example.com/', 'image_path': ''}

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], str(self.project.pk))
        self.assertFalse(response.data[0]['is_starred'])
        self.assertNotIn('fields', response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertFalse(ProjectSerializer(self.project).data['is_starred'])

    def test_search_and_empty_results(self):
        self.assertEqual(len(self.client.get(self.list_url, {'title': ' PORT '}).data), 1)
        self.assertEqual(self.client.get(self.list_url, {'title': 'not-found'}).data, [])

    def test_missing_project(self):
        self.assertEqual(self.client.get(reverse('api:project-detail', args=[uuid.uuid4()])).status_code, 404)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format='json').status_code, 403)
            for method in ('put', 'patch', 'delete'):
                self.assertEqual(getattr(self.client, method)(self.detail_url, self.payload, format='json').status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Portfolio')

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(pk=response.data['id']).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [({'title': '   '}, 'title'),
                               ({'title': '<img src="x" onerror="alert(1)">'}, 'title'),
                               ({'link': 'javascript:alert(1)'}, 'link'),
                               ({'link_2': 'invalid'}, 'link_2'),
                               ({'project_type': 'invalid'}, 'project_type')]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {'title': 'Changed'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, 'My website')
        # Only title is required by this project's existing model.
        self.assertEqual(self.client.put(self.detail_url, {'description': 'Missing title'}, format='json').status_code, 400)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format='json').status_code, 200)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url, {'starred_by': [self.owner.pk]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['is_starred'])
        self.assertEqual(response.data['star_count'], 1)
        self.assertEqual(response.data['starred_by_names'], 'visitor')
        self.assertFalse(self.project.starred_by.filter(pk=self.owner.pk).exists())
        response = self.client.post(self.star_url)
        self.assertFalse(response.data['is_starred'])
        self.assertEqual(response.data['star_count'], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {**self.payload, 'id': str(self.project.pk),
            'star_count': 99, 'is_starred': True, 'starred_by_names': 'forged',
            'starred_by': [self.visitor.pk]}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data['id'], str(self.project.pk))
        self.assertEqual(response.data['star_count'], 0)
        self.assertFalse(response.data['is_starred'])
        self.assertEqual(response.data['starred_by_names'], '')

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name='Editor'))
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.patch(self.detail_url, {'title': 'Changed'}, format='json').status_code, 403)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username='owner', password='test-password'))
        self.assertEqual(client.post(self.list_url, self.payload, format='json').status_code, 403)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='owner', password='test-password')
        self.assertEqual(client.get(self.list_url, HTTP_ACCEPT='text/html').status_code, 200)
        response = client.post(self.list_url, self.payload, format='json',
                               HTTP_X_CSRFTOKEN=client.cookies['csrftoken'].value)
        self.assertEqual(response.status_code, 201)


class ExperienceAPITest(APITestCase):
    def setUp(self):
        Experience.objects.all().delete()
        self.owner = User.objects.create_superuser('owner', 'owner@example.com', 'test-password')
        self.editor = User.objects.create_user('editor', password='test-password')
        self.editor.groups.add(Group.objects.create(name='Editor'))
        self.visitor = User.objects.create_user('visitor', password='test-password')
        self.experience = Experience.objects.create(title='Developer', company='Example', category='internship')
        self.list_url = reverse('api:experience-list')
        self.detail_url = reverse('api:experience-detail', args=[self.experience.pk])
        self.star_url = reverse('api:experience-star', args=[self.experience.pk])

    def test_public_read_search_and_missing(self):
        response = self.client.get(self.list_url, {'title': 'DEVEL'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['category_display'], 'Internship')
        self.assertTrue(response.data[0]['is_ongoing'])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertEqual(self.client.get(self.list_url, {'title': 'absent'}).data, [])
        self.assertEqual(self.client.get(reverse('api:experience-detail', args=[uuid.uuid4()])).status_code, 404)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        for method in ('put', 'patch'):
            response = getattr(self.client, method)(self.detail_url, {'title': 'Edited'}, format='json')
            self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, 'Edited')
        self.assertEqual(self.experience.company, 'Example')
        self.assertEqual(self.client.post(self.list_url, {'title': 'No'}, format='json').status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_guest_and_visitor_cannot_manage(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, {'title': 'No'}, format='json').status_code, 403)
            for method in ('put', 'patch', 'delete'):
                self.assertEqual(getattr(self.client, method)(self.detail_url, {'title': 'No'}, format='json').status_code, 403)

    def test_owner_crud_validation_and_read_only_fields(self):
        self.client.force_authenticate(user=self.owner)
        for payload in ({'title': '<b></b>'}, {'title': 'New', 'category': 'invalid'}):
            self.assertEqual(self.client.post(self.list_url, payload, format='json').status_code, 400)
        response = self.client.post(self.list_url, {'title': '<b>New</b>', 'category': 'organization',
            'company': '<i>Company</i>', 'stars': [self.editor.pk], 'star_count': 50, 'is_ongoing': False}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'New')
        self.assertEqual(response.data['company'], 'Company')
        self.assertEqual(response.data['star_count'], 0)
        self.assertTrue(response.data['is_ongoing'])
        self.assertEqual(self.client.patch(self.detail_url, {'ended_at': '2026'}, format='json').status_code, 200)
        self.assertFalse(self.client.get(self.detail_url).data['is_ongoing'])
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')

    def test_star_uses_authenticated_account(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        for user in (self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.star_url, {'stars': [self.owner.pk]}, format='json')
            self.assertTrue(response.data['is_starred'])
            self.assertEqual(response.data['star_count'], 1)
            self.assertEqual(response.data['starred_by_names'], user.username)
            self.assertEqual(self.client.post(self.star_url).data['star_count'], 0)

    def test_safe_methods_do_not_mutate(self):
        for url in (self.list_url, self.detail_url):
            self.assertEqual(self.client.head(url).status_code, 200)
            self.assertEqual(self.client.options(url).status_code, 200)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(self.experience.stars.count(), 0)

    def test_session_csrf_on_both_pages_and_star_endpoints(self):
        project = Project.objects.create(title='CSRF project')
        for page, endpoint in [('main:show_experiences', self.star_url),
                ('main:show_projects', reverse('api:project-star', args=[project.pk]))]:
            client = APIClient(enforce_csrf_checks=True)
            client.login(username='visitor', password='test-password')
            self.assertEqual(client.post(endpoint).status_code, 403)
            response = client.get(reverse(page))
            self.assertEqual(response.status_code, 200)
            self.assertIn('csrftoken', client.cookies)
            self.assertEqual(client.post(endpoint, HTTP_X_CSRFTOKEN=client.cookies['csrftoken'].value).status_code, 200)

    def test_invalid_json_and_permission_before_lookup(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.post(self.list_url, '{broken', content_type='application/json').status_code, 400)
        self.client.force_authenticate(user=self.visitor)
        missing = reverse('api:experience-detail', args=[uuid.uuid4()])
        self.assertEqual(self.client.patch(missing, {'title': 'No'}, format='json').status_code, 403)
