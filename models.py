from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

SII_STATUS = [
    ('pending', _('Pending')),
    ('submitted', _('Submitted')),
    ('accepted', _('Accepted')),
    ('rejected', _('Rejected')),
]

class SIISubmission(HubBaseModel):
    reference = models.CharField(max_length=50, verbose_name=_('Reference'))
    submission_type = models.CharField(max_length=30, verbose_name=_('Submission Type'))
    period = models.CharField(max_length=10, verbose_name=_('Period'))
    status = models.CharField(max_length=20, default='pending', choices=SII_STATUS, verbose_name=_('Status'))
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Submitted At'))
    response_code = models.CharField(max_length=50, blank=True, verbose_name=_('Response Code'))
    response_message = models.TextField(blank=True, verbose_name=_('Response Message'))
    records_count = models.PositiveIntegerField(default=0, verbose_name=_('Records Count'))

    class Meta(HubBaseModel.Meta):
        db_table = 'sii_siisubmission'

    def __str__(self):
        return self.reference

