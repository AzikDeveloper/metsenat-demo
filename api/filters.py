from rest_framework import filters


class DateRangeFilterBackend(filters.BaseFilterBackend):
    """
        Filters queryset between two dates by their DateField fields
        'date_range_filter_fields' should be declared in view class.

        Usage example:
        hostname/api/resource?date_field-gte=2021-12-10&date_field-lte=2021-12-19
        this means that 'date_field' is between 2021-12-10 and 2021-12-19
        note that both are included too.
    """

    def filter_queryset(self, request, queryset, view):
        date_fields = view.date_range_filter_fields
        filter_mask = {}
        for date_field in date_fields:
            date_field__gte = date_field + '__gte'
            date_field__lte = date_field + '__lte'
            date_field_gte = date_field + '-gte'
            date_field_lte = date_field + '-lte'
            if date_field_gte in request.query_params:
                filter_mask[date_field__gte] = request.query_params[date_field_gte]
            if date_field_lte in request.query_params:
                filter_mask[date_field__lte] = request.query_params[date_field_lte]

        queryset = queryset.filter(**filter_mask)
        return queryset
