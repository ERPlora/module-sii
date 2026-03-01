"""AI tools for the SII module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListSIISubmissions(AssistantTool):
    name = "list_sii_submissions"
    description = "List SII (Suministro Inmediato de Información) submissions."
    module_id = "sii"
    required_permission = "sii.view_siisubmission"
    parameters = {"type": "object", "properties": {"status": {"type": "string", "description": "pending, submitted, accepted, rejected"}, "period": {"type": "string"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from sii.models import SIISubmission
        qs = SIISubmission.objects.all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        if args.get('period'):
            qs = qs.filter(period=args['period'])
        return {"submissions": [{"id": str(s.id), "reference": s.reference, "submission_type": s.submission_type, "period": s.period, "status": s.status, "records_count": s.records_count} for s in qs.order_by('-created_at')]}


@register_tool
class GetSIISubmission(AssistantTool):
    name = "get_sii_submission"
    description = "Get detailed SII submission info including response code and message."
    module_id = "sii"
    required_permission = "sii.view_siisubmission"
    parameters = {
        "type": "object",
        "properties": {"submission_id": {"type": "string", "description": "Submission ID"}},
        "required": ["submission_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from sii.models import SIISubmission
        s = SIISubmission.objects.get(id=args['submission_id'])
        return {
            "id": str(s.id), "reference": s.reference,
            "submission_type": s.submission_type, "period": s.period,
            "status": s.status, "records_count": s.records_count,
            "submitted_at": s.submitted_at.isoformat() if s.submitted_at else None,
            "response_code": s.response_code, "response_message": s.response_message,
        }


@register_tool
class CreateSIISubmission(AssistantTool):
    name = "create_sii_submission"
    description = "Create a new SII submission for a tax period."
    module_id = "sii"
    required_permission = "sii.add_siisubmission"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "submission_type": {"type": "string", "description": "Type: issued_invoices, received_invoices"},
            "period": {"type": "string", "description": "Tax period (e.g. 2026-01, 2026-Q1)"},
            "reference": {"type": "string", "description": "Submission reference"},
        },
        "required": ["submission_type", "period"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from sii.models import SIISubmission
        s = SIISubmission.objects.create(
            submission_type=args['submission_type'],
            period=args['period'],
            reference=args.get('reference', ''),
            status='pending',
        )
        return {"id": str(s.id), "reference": s.reference, "status": "pending", "created": True}


@register_tool
class GetSIISummary(AssistantTool):
    name = "get_sii_summary"
    description = "Get SII submission summary: counts by status for a period."
    module_id = "sii"
    required_permission = "sii.view_siisubmission"
    parameters = {
        "type": "object",
        "properties": {"period": {"type": "string", "description": "Tax period to summarize"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from sii.models import SIISubmission
        qs = SIISubmission.objects.all()
        if args.get('period'):
            qs = qs.filter(period=args['period'])
        result = {}
        for status in ('pending', 'submitted', 'accepted', 'rejected'):
            result[status] = qs.filter(status=status).count()
        result['total'] = qs.count()
        return result
