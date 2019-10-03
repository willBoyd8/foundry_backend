from django.urls import path
from . import register_endpoints

register_functions = [
    path(r'register_realtor/', register_endpoints.RegisterRealtorView.as_view(), name='register_realtor'),
    path(r'register_admin/', register_endpoints.RegisterAdminView.as_view(), name='register_admin'),
    path(r'unregister_admin/', register_endpoints.UnRegisterAdminView.as_view(), name='unregister_admin')
]
