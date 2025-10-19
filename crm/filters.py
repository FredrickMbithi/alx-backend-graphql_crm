from django_filters import FilterSet
from .models import Customer


class CustomerFilter(FilterSet):
    class Meta:
        model = Customer
        fields = ['name', 'email']
