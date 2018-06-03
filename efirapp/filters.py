from .models import *
import django_filters

class CompFilter(django_filters.FilterSet):
    class Meta:
        model = Complaint
        fields = {'state' : ['exact', ], 'city':['exact'], }

