"""
SII (Spain) Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import SIISubmission

PER_PAGE_CHOICES = [12, 24, 48, 96, 0]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('sii', 'dashboard')
@htmx_view('sii/pages/index.html', 'sii/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_sii_submissions': SIISubmission.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# SIISubmission
# ======================================================================

SII_SUBMISSION_SORT_FIELDS = {
    'reference': 'reference',
    'status': 'status',
    'records_count': 'records_count',
    'submission_type': 'submission_type',
    'period': 'period',
    'submitted_at': 'submitted_at',
    'created_at': 'created_at',
}

def _build_sii_submissions_context(hub_id, per_page=10):
    qs = SIISubmission.objects.filter(hub_id=hub_id, is_deleted=False).order_by('reference')
    paginator = Paginator(qs, per_page if per_page > 0 else max(qs.count(), 1))
    page_obj = paginator.get_page(1)
    return {
        'sii_submissions': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'reference',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_sii_submissions_list(request, hub_id, per_page=10):
    ctx = _build_sii_submissions_context(hub_id, per_page)
    return django_render(request, 'sii/partials/sii_submissions_list.html', ctx)

@login_required
@with_module_nav('sii', 'submissions')
@htmx_view('sii/pages/sii_submissions.html', 'sii/partials/sii_submissions_content.html')
def sii_submissions_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'reference')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 12))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 12

    qs = SIISubmission.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(reference__icontains=search_query) | Q(submission_type__icontains=search_query) | Q(period__icontains=search_query) | Q(status__icontains=search_query))

    order_by = SII_SUBMISSION_SORT_FIELDS.get(sort_field, 'reference')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['reference', 'status', 'records_count', 'submission_type', 'period', 'submitted_at']
        headers = ['Reference', 'Status', 'Records Count', 'Submission Type', 'Period', 'Submitted At']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='sii_submissions.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='sii_submissions.xlsx')

    paginator = Paginator(qs, per_page if per_page > 0 else max(qs.count(), 1))
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'sii/partials/sii_submissions_list.html', {
            'sii_submissions': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'sii_submissions': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
@htmx_view('sii/pages/sii_submission_add.html', 'sii/partials/sii_submission_add_content.html')
def sii_submission_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        reference = request.POST.get('reference', '').strip()
        submission_type = request.POST.get('submission_type', '').strip()
        period = request.POST.get('period', '').strip()
        status = request.POST.get('status', '').strip()
        submitted_at = request.POST.get('submitted_at') or None
        response_code = request.POST.get('response_code', '').strip()
        response_message = request.POST.get('response_message', '').strip()
        records_count = int(request.POST.get('records_count', 0) or 0)
        obj = SIISubmission(hub_id=hub_id)
        obj.reference = reference
        obj.submission_type = submission_type
        obj.period = period
        obj.status = status
        obj.submitted_at = submitted_at
        obj.response_code = response_code
        obj.response_message = response_message
        obj.records_count = records_count
        obj.save()
        response = HttpResponse(status=204)
        response['HX-Redirect'] = reverse('sii:sii_submissions_list')
        return response
    return {}

@login_required
@htmx_view('sii/pages/sii_submission_edit.html', 'sii/partials/sii_submission_edit_content.html')
def sii_submission_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(SIISubmission, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.reference = request.POST.get('reference', '').strip()
        obj.submission_type = request.POST.get('submission_type', '').strip()
        obj.period = request.POST.get('period', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.submitted_at = request.POST.get('submitted_at') or None
        obj.response_code = request.POST.get('response_code', '').strip()
        obj.response_message = request.POST.get('response_message', '').strip()
        obj.records_count = int(request.POST.get('records_count', 0) or 0)
        obj.save()
        return _render_sii_submissions_list(request, hub_id)
    return {'obj': obj}

@login_required
@require_POST
def sii_submission_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(SIISubmission, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_sii_submissions_list(request, hub_id)

@login_required
@require_POST
def sii_submissions_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = SIISubmission.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_sii_submissions_list(request, hub_id)


@login_required
@permission_required('sii.manage_settings')
@with_module_nav('sii', 'settings')
@htmx_view('sii/pages/settings.html', 'sii/partials/settings_content.html')
def settings_view(request):
    return {}

