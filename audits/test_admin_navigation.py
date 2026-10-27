from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse


class AdminNavigationTests(TestCase):
    def test_staff_can_find_user_administration(self):
        user = User.objects.create_superuser('admin', password='test-password')
        self.client.force_login(user)
        self.assertContains(self.client.get('/'), 'href="/admin/"')
        self.assertEqual(self.client.get(reverse('admin:auth_user_add')).status_code, 200)

    def test_reader_has_no_admin_link_or_user_management_access(self):
        user = User.objects.create_user('reader', password='test-password')
        user.user_permissions.add(Permission.objects.get(codename='view_audit'))
        self.client.force_login(user)
        self.assertNotContains(self.client.get('/'), 'href="/admin/"')
        self.assertEqual(self.client.get(reverse('admin:auth_user_add')).status_code, 302)
