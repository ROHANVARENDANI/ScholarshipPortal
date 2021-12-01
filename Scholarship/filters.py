import django_filters

from .models import *

class ScholarshipFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Scholarship
        fields = ['timestamp', 'start_date', 'end_date', 'financial_coverage', 'category', 'field_of_studies']