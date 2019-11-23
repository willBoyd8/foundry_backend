import django_filters

from foundry_backend.database import models


class ListingFilterSet(django_filters.FilterSet):
    square_footage_min = django_filters.NumberFilter(field_name='property__square_footage', lookup_expr='gte')
    square_footage = django_filters.NumberFilter(field_name='property__square_footage', lookup_expr='exact')
    square_footage_max = django_filters.NumberFilter(field_name='property__square_footage', lookup_expr='lte')

    asking_price_min = django_filters.NumberFilter(field_name='asking_price', lookup_expr='gte')
    asking_price = django_filters.NumberFilter(field_name='asking_price', lookup_expr='exact')
    asking_price_max = django_filters.NumberFilter(field_name='asking_price', lookup_expr='lte')

    zip_code = django_filters.CharFilter(field_name='property__address__postal_code', lookup_expr='exact')

    open = django_filters.BooleanFilter(field_name='open', lookup_expr='exact')

    class Meta:
        model = models.Listing
        fields = [
            'asking_price_min', 'asking_price', 'asking_price_max',
            'square_footage_min', 'square_footage', 'square_footage_max',
            'zip_code',
            'open'
        ]


class ListingsHitFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.ListingsHit
        fields = ['listing', 'access_time']


class ListingImageFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.ListingImage
        fields = ['listing']


class AgencyFilterSet(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='address__locality', lookup_expr='iexact')
    state = django_filters.CharFilter(field_name='address__state_code', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='iexact')

    class Meta:
        model = models.Agency
        fields = ['city', 'state', 'name', 'phone']


class MLSNumberFilterSet(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='agency__address__locality', lookup_expr='iexact')
    agency = django_filters.CharFilter(field_name='agency__name', lookup_expr='iexact')
    mls_number = django_filters.CharFilter(field_name='number', lookup_expr='iexact')

    class Meta:
        model = models.MLSNumber
        fields = ['city', 'agency', 'mls_number']


class ShowingReviewFilterSet(django_filters.FilterSet):
    agent = django_filters.NumberFilter(field_name='agent', lookup_expr='exact',
                                        help_text='Show only surveys for the given agent')
    showing = django_filters.NumberFilter(field_name='showing', lookup_expr='exact',
                                          help_text='Show only surveys for the given showing')

    class Meta:
        model = models.ShowingReview
        fields = ['agent', 'showing']
