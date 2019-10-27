from django.conf.urls import url
from django.urls import include, path
from rest_framework_nested import routers

from foundry_backend.api import views
from .endpoints import permissions_functions

# router = routers.DefaultRouter()
# router.register(r'nearby_attractions', views.NearbyAttractionViewSet)
# router.register(r'nearby_property_attraction_connectors', views.NearbyAttractionPropertyConnectorViewSet)
# router.register(r'rooms', views.RoomViewSet)
# router.register(r'home_alarms', views.HomeAlarmViewSet)
# router.register(r'showings', views.HomeAlarmViewSet)

base_router = routers.SimpleRouter()

# register IAM policies
base_router.register(r'iam_policies', views.IAMPolicyViewSet)

policies_router = routers.NestedSimpleRouter(base_router, r'iam_policies', lookup='policy')
policies_router.register(r'rules', views.IAMPolicyStatementViewSet, )

policies_statement_router = routers.NestedSimpleRouter(policies_router, r'rules', lookup='rule')
policies_statement_router.register(r'principals', views.IAMPolicyStatementPrincipalViewSet)
policies_statement_router.register(r'conditions', views.IAMPolicyStatementConditionViewSet)

# register Agencies
base_router.register(r'agencies', views.AgencyViewSet)

agencies_router = routers.NestedSimpleRouter(base_router, r'agencies', lookup='agency')
agencies_router.register(r'mls_numbers', views.MLSNumberViewSet)

# register listings
base_router.register(r'listings', views.ListingViewSet)

listings_router = routers.NestedSimpleRouter(base_router, r'listings', lookup='listing')
listings_router.register(r'property', views.PropertyViewSet)

property_router = routers.NestedSimpleRouter(listings_router, r'property', lookup='property')
property_router.register(r'rooms', views.RoomViewSet)
property_router.register(r'nearby_attractions', views.NearbyAttractionViewSet)

# register nearby attractions
base_router.register(r'nearby_attractions', views.AllNearbyAttractionsViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path(r'', include(base_router.urls)),
    path(r'', include(policies_router.urls)),
    path(r'', include(policies_statement_router.urls)),
    path(r'', include(agencies_router.urls)),
    path(r'', include(listings_router.urls)),
    path(r'', include(property_router.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^auth/permissions/', include(permissions_functions))
]

# # Create the groups
# _, created = Group.objects.get_or_create(name='admins')
# if created:
#     print('Created Admin Group')
