from django.urls import path
from . import views

app_name = 'sii'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('submissions/', views.submissions, name='submissions'),
    path('settings/', views.settings, name='settings'),
]
