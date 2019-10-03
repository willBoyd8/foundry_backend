from django.conf.urls import url
from django.contrib.auth.models import Group
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions
from . import views
from .endpoints import register_functions

router = routers.DefaultRouter()
router.register(r'agencies', views.AgencyViewSet)
router.register(r'mls_numbers', views.MLSNumberViewSet)
router.register(r'realtors', views.RealtorUserViewSet)
router.register(r'listings', views.ListingViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Foundry MLS",
        default_version='v1',
        description="The Backend for Foundry",
        terms_of_service="http://www.placekitten.com/400/400",
        contact=openapi.Contact(email="foundry@abwlabs.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('', RedirectView.as_view(url='swagger/')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', include(register_functions))
]

# Create the groups
_, created = Group.objects.get_or_create(name='admins')
if created:
    print('Created Admin Group')
