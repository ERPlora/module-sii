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
