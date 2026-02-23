"""
SII (Spain) Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('sii', 'dashboard')
@htmx_view('sii/pages/dashboard.html', 'sii/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('sii', 'submissions')
@htmx_view('sii/pages/submissions.html', 'sii/partials/submissions_content.html')
def submissions(request):
    """Submissions view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('sii', 'settings')
@htmx_view('sii/pages/settings.html', 'sii/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

