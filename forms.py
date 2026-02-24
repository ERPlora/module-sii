from django import forms
from django.utils.translation import gettext_lazy as _

from .models import SIISubmission

class SIISubmissionForm(forms.ModelForm):
    class Meta:
        model = SIISubmission
        fields = ['reference', 'submission_type', 'period', 'status', 'submitted_at', 'response_code', 'response_message', 'records_count']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'submission_type': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'period': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'submitted_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'response_code': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'response_message': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'records_count': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

