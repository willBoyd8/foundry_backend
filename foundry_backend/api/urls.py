from django.conf.urls import url
from django.urls import include, path
from rest_framework_nested import routers

from foundry_backend.api import views
from .endpoints import permissions_functions

router = routers.DefaultRouter()
router.register(r'agencies', views.AgencyViewSet)
router.register(r'mls_numbers', views.MLSNumberViewSet)
router.register(r'nearby_attractions', views.NearbyAttractionViewSet)
router.register(r'properties', views.PropertyViewSet)
router.register(r'nearby_property_attraction_connectors', views.NearbyAttractionPropertyConnectorViewSet)
router.register(r'listings', views.ListingViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'home_alarms', views.HomeAlarmViewSet)
router.register(r'showings', views.HomeAlarmViewSet)
# router.register(r'iam', views.IAMPolicyViewSet)

base_router = routers.SimpleRouter()

base_router.register(r'iam_policies', views.IAMPolicyViewSet)

policies_router = routers.NestedSimpleRouter(base_router, r'iam_policies', lookup='policy')
policies_router.register(r'rules', views.IAMPolicyStatementViewSet, )

policies_statement_router = routers.NestedSimpleRouter(policies_router, r'rules', lookup='rule')
policies_statement_router.register(r'principals', views.IAMPolicyStatementPrincipalViewSet)
policies_statement_router.register(r'conditions', views.IAMPolicyStatementConditionViewSet)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path(r'', include(base_router.urls)),
    path(r'', include(policies_router.urls)),
    path(r'', include(policies_statement_router.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^auth/permissions/', include(permissions_functions))
]

# # Create the groups
# _, created = Group.objects.get_or_create(name='admins')
# if created:
#     print('Created Admin Group')
