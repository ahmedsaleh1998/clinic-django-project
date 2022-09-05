from turtle import title
import django_filters
from .models import Appointments

class AppointFilter(django_filters.FilterSet):
    # description = django_filters.CharFilter(lookup_expr='icontains')
    # title = django_filters.CharFilter(lookup_expr='icontains')
    # location = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Appointments
        fields = ['user','date','time','state']