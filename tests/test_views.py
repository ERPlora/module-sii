"""Tests for sii views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('sii:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('sii:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('sii:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSIISubmissionViews:
    """SIISubmission view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('sii:sii_submissions_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('sii:sii_submissions_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('sii:sii_submissions_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('sii:sii_submissions_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('sii:sii_submissions_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('sii:sii_submissions_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('sii:sii_submission_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('sii:sii_submission_add')
        data = {
            'reference': 'New Reference',
            'submission_type': 'New Submission Type',
            'period': 'New Period',
            'status': 'New Status',
            'submitted_at': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, sii_submission):
        """Test edit form loads."""
        url = reverse('sii:sii_submission_edit', args=[sii_submission.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, sii_submission):
        """Test editing via POST."""
        url = reverse('sii:sii_submission_edit', args=[sii_submission.pk])
        data = {
            'reference': 'Updated Reference',
            'submission_type': 'Updated Submission Type',
            'period': 'Updated Period',
            'status': 'Updated Status',
            'submitted_at': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, sii_submission):
        """Test soft delete via POST."""
        url = reverse('sii:sii_submission_delete', args=[sii_submission.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        sii_submission.refresh_from_db()
        assert sii_submission.is_deleted is True

    def test_bulk_delete(self, auth_client, sii_submission):
        """Test bulk delete."""
        url = reverse('sii:sii_submissions_bulk_action')
        response = auth_client.post(url, {'ids': str(sii_submission.pk), 'action': 'delete'})
        assert response.status_code == 200
        sii_submission.refresh_from_db()
        assert sii_submission.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('sii:sii_submissions_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('sii:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('sii:settings')
        response = client.get(url)
        assert response.status_code == 302

