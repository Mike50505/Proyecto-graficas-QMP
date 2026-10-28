from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .importer import confirm, preview
from .models import Audit, Importation
from .tests import excel, row


class ImportationDeletionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('operator', password='test-password')
        self.first, _ = confirm(preview(excel([row(ID='A'), row(ID='B')]), 'first.xlsx'), self.user)
        self.other, _ = confirm(preview(excel([row(ID='C')]), 'other.xlsx'), self.user)
        self.url = reverse('delete-importation', args=[self.first.pk])
        self.client.force_login(self.user)

    def test_confirmation_does_not_delete_and_shows_full_count(self):
        response = self.client.get(self.url, {'semana': '2026-W44'})
        self.assertContains(response, 'first.xlsx')
        self.assertEqual(response.context['audit_count'], 2)
        self.assertEqual(self.first.audits.count(), 2)

    def test_confirmed_delete_only_removes_selected_import_and_clears_session(self):
        session = self.client.session
        session['active_import'] = self.first.pk
        session.save()
        response = self.client.post(self.url, {'confirmar': 'eliminar'})
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Importation.objects.filter(pk=self.first.pk).exists())
        self.assertFalse(Audit.objects.filter(importation_id=self.first.pk).exists())
        self.assertTrue(self.other.audits.exists())
        self.assertEqual(self.client.session['active_import'], self.other.pk)

    def test_missing_confirmation_cannot_delete(self):
        self.assertEqual(self.client.post(self.url).status_code, 400)
        self.assertTrue(Importation.objects.filter(pk=self.first.pk).exists())

    def test_login_and_csrf_are_required(self):
        self.client.logout()
        self.assertEqual(self.client.post(self.url, {'confirmar': 'eliminar'}).status_code, 302)
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)
        self.assertEqual(csrf_client.post(self.url, {'confirmar': 'eliminar'}).status_code, 403)
        self.assertTrue(Importation.objects.filter(pk=self.first.pk).exists())

    def test_deleting_last_import_shows_empty_dashboard(self):
        self.other.delete()
        response = self.client.post(self.url, {'confirmar': 'eliminar'}, follow=True)
        self.assertContains(response, 'Aún no hay importaciones')

    def test_deleted_file_can_be_imported_again(self):
        self.client.post(self.url, {'confirmar': 'eliminar'})
        imported, created = confirm(preview(excel([row(ID='A'), row(ID='B')]), 'first.xlsx'), self.user)
        self.assertTrue(created)
        self.assertEqual(imported.audits.count(), 2)
