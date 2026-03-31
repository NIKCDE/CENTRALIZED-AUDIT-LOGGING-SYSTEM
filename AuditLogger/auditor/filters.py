import django_filters
from .models import AuditLog


class AuditLogFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = AuditLog
        fields = ['user', 'action', 'status']