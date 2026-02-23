from django.contrib import admin

from .models import SIISubmission

@admin.register(SIISubmission)
class SIISubmissionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'submission_type', 'period', 'status', 'submitted_at']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

