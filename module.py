from django.utils.translation import gettext_lazy as _

MODULE_ID = 'sii'
MODULE_NAME = _('SII (Spain)')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'shield-outline'
MODULE_DESCRIPTION = _('Suministro Inmediato de Información — real-time VAT reporting for Spain')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'compliance'

MENU = {
    'label': _('SII (Spain)'),
    'icon': 'shield-outline',
    'order': 80,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Submissions'), 'icon': 'shield-outline', 'id': 'submissions'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'sii.view_siisubmission',
'sii.submit_sii',
'sii.manage_settings',
]

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": [
        "submit_sii",
        "view_siisubmission",
    ],
    "employee": [
        "view_siisubmission",
    ],
}
