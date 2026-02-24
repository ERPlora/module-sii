from django.urls import path
from . import views

app_name = 'sii'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # SIISubmission
    path('sii_submissions/', views.sii_submissions_list, name='sii_submissions_list'),
    path('sii_submissions/add/', views.sii_submission_add, name='sii_submission_add'),
    path('sii_submissions/<uuid:pk>/edit/', views.sii_submission_edit, name='sii_submission_edit'),
    path('sii_submissions/<uuid:pk>/delete/', views.sii_submission_delete, name='sii_submission_delete'),
    path('sii_submissions/bulk/', views.sii_submissions_bulk_action, name='sii_submissions_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
