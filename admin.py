from django.contrib import admin

from .models import SIISubmission

@admin.register(SIISubmission)
class SIISubmissionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'submission_type', 'period', 'status', 'submitted_at', 'created_at']
    search_fields = ['reference', 'submission_type', 'period', 'status']
    readonly_fields = ['created_at', 'updated_at']

