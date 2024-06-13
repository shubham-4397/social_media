from django.db.models import Q
from django_filters import rest_framework as filters


class NameEmailFilters(filters.FilterSet):
    """
    Filter either by name or email.
    """
    search = filters.CharFilter()

    def filter_queryset(self, queryset):
        search = self.data.get('search')
        filter_query = Q()
        if search:
            if '@' in search:
                filter_query &= Q(email__iexact=search)
            else:
                filter_query &= (Q(first_name__icontains=search) | Q(last_name__icontains=search))
        return queryset.filter(filter_query)
