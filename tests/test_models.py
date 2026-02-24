"""Tests for sii models."""
import pytest
from django.utils import timezone

from sii.models import SIISubmission


@pytest.mark.django_db
class TestSIISubmission:
    """SIISubmission model tests."""

    def test_create(self, sii_submission):
        """Test SIISubmission creation."""
        assert sii_submission.pk is not None
        assert sii_submission.is_deleted is False

    def test_str(self, sii_submission):
        """Test string representation."""
        assert str(sii_submission) is not None
        assert len(str(sii_submission)) > 0

    def test_soft_delete(self, sii_submission):
        """Test soft delete."""
        pk = sii_submission.pk
        sii_submission.is_deleted = True
        sii_submission.deleted_at = timezone.now()
        sii_submission.save()
        assert not SIISubmission.objects.filter(pk=pk).exists()
        assert SIISubmission.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, sii_submission):
        """Test default queryset excludes deleted."""
        sii_submission.is_deleted = True
        sii_submission.deleted_at = timezone.now()
        sii_submission.save()
        assert SIISubmission.objects.filter(hub_id=hub_id).count() == 0


