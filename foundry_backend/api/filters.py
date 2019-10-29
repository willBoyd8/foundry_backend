import django_filters

from foundry_backend.database import models


# class AddressFilterSet(django_filters.FilterSet):
#     class Meta:
#         model = models.Address
#         fields = {
#             'postal_code': ['exact']
#         }
#
#
# class PropertyFilterSet(django_filters.FilterSet):
#     address_filter = AddressFilterSet()
#
#     class Meta:
#         model = models.Property
#         fields = {
#             'postal_code': ['exact'],
#             'square_footage': ['gte', 'lte', 'exact']
#         }


class ListingFilterSet(django_filters.FilterSet):
    square_footage_min = django_filters.NumberFilter(field_name='property__square_footage', lookup_expr='gte')
    square_footage = django_filters.NumberFilter(field_name='property__square_footage', lookup_expr='exact')
    square_footage_max = django_filters.NumberFilter(field_name='property__square_footage', lookup_expr='lte')

    asking_price_min = django_filters.NumberFilter(field_name='asking_price', lookup_expr='gte')
    asking_price = django_filters.NumberFilter(field_name='asking_price', lookup_expr='exact')
    asking_price_max = django_filters.NumberFilter(field_name='asking_price', lookup_expr='lte')

    zip_code = django_filters.NumericRangeFilter(field_name='property__address__postal_code')

    class Meta:
        model = models.Listing
        fields = ['asking_price_min', 'asking_price', 'asking_price_max',
                  'square_footage_min', 'square_footage', 'square_footage_max',
                  'zip_code']
