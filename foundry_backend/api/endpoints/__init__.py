from django.urls import path
from . import register_endpoints
from . import generate_contracts

permissions_functions = [
    path(r'enable_realtor/', register_endpoints.EnableRealtorView.as_view(), name='enable_realtor'),
    path(r'enable_admin/', register_endpoints.EnableAdminView.as_view(), name='enable_admin'),
    path(r'disable_admin/', register_endpoints.DisableAdminView.as_view(), name='disable_admin')
]

# legal_functions = [
#     path(r'sales_contract/', generate_contracts.GenerateSalesContractView.as_view(), name='sales_contract'),
#     path(r'request_for_repairs/', generate_contracts.GenerateRequestForRepairsView.as_view(),
#          name='request_for_repairs'),
# ]

# legal_functions = [
#     generate_contracts.generate_endpoint_for_legal_template('request_for_repairs.html'),
#     generate_contracts.generate_endpoint_for_legal_template('sales_contract.html')
# ]

legal_functions = generate_contracts.get_all_legal_template_endpoints()
