# AaryaOnlineCompiler - Compiler App URL Configuration
# Created by Aarya Agarwal

from django.urls import path
from . import views

urlpatterns = [
    path('execute/', views.ExecuteCodeView.as_view(), name='execute_code'),
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
]
