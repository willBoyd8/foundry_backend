from django.urls import path
from . import register_endpoints

permissions_functions = [
    path(r'enable_realtor/', register_endpoints.EnableRealtorView.as_view(), name='enable_realtor'),
    path(r'enable_admin/', register_endpoints.EnableAdminView.as_view(), name='enable_admin'),
    path(r'disable_admin/', register_endpoints.DisableAdminView.as_view(), name='disable_admin')
]
