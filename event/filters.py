from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.widgets import RangeWidget
from drf_yasg.inspectors import CoreAPICompatInspector, NotHandled

from event.models import Event


class DjangoFilterDescriptionInspector(CoreAPICompatInspector):
    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, DjangoFilterBackend):
            result = super(DjangoFilterDescriptionInspector, self).get_filter_parameters(filter_backend)
            for param in result:
                if not param.get('description', ''):
                    param.description = "Filter the returned list by {field_name}".format(field_name=param.name)
            return result
        return NotHandled


class EventFilter(filters.FilterSet):
    datetime_after = filters.DateTimeFilter(field_name="datetime_created", lookup_expr='gte',
                                            label="After datetime (e.g. 2018-12-08T16:24:10)")
    datetime_before = filters.DateTimeFilter(field_name="datetime_created", lookup_expr='lte',
                                             label="Before datetime (e.g. 2018-12-08T16:24:10)")
    latitude = filters.NumericRangeFilter(field_name="latitude", widget=RangeWidget())
    longitude = filters.NumericRangeFilter(field_name="longitude", widget=RangeWidget())

    class Meta:
        model = Event
        fields = ['country_name', 'country_iso', 'latitude', 'longitude', 'city', 'datetime_before', 'datetime_after']
