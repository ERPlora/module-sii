from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SiiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sii'
    label = 'sii'
    verbose_name = _('SII (Spain)')

    def ready(self):
        pass
