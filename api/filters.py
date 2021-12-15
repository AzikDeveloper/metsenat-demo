from rest_framework import filters


class DateRangeFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        date_field = view.date_range_filter_field
        date_field_gte = date_field + '__gte'
        date_field_lte = date_field + '__lte'

        filter_mask = {}
        if 'start_date' in request.query_params:
            filter_mask[date_field_gte] = request.query_params['start_date']
        if 'end_date' in request.query_params:
            filter_mask[date_field_lte] = request.query_params['end_date']

        queryset = queryset.filter(**filter_mask)
        return queryset
