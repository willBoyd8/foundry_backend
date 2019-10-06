from django.conf.urls import url
from django.contrib.auth.models import Group
from django.urls import include, path
from rest_framework import routers
from . import views
from .endpoints import register_functions

router = routers.DefaultRouter()
router.register(r'agencies', views.AgencyViewSet)
router.register(r'mls_numbers', views.MLSNumberViewSet)
router.register(r'realtors', views.RealtorUserViewSet)
router.register(r'nearby_attraction', views.NearbyAttractionViewSet)
router.register(r'properties', views.PropertyViewSet)
router.register(r'nearby_property_attraction_connectors', views.NearbyAttractionPropertyConnectorViewSet)
router.register(r'listings', views.ListingViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    path('register/', include(register_functions))
]

# # Create the groups
# _, created = Group.objects.get_or_create(name='admins')
# if created:
#     print('Created Admin Group')
