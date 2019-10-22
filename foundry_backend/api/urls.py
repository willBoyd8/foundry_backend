from django.conf.urls import url
from django.contrib.auth.models import Group
from django.urls import include, path
from rest_framework import routers

from . import views
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
router.register(r'iam', views.IAMPolicyViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^auth/permissions/', include(permissions_functions))
]

# # Create the groups
# _, created = Group.objects.get_or_create(name='admins')
# if created:
#     print('Created Admin Group')
