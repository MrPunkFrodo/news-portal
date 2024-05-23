from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post


class NewsFilter(FilterSet):
    published_after = DateTimeFilter(
        field_name='date_created',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%d',
            attrs={'type': 'datetime-local'},
        )
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'postCategory': ['exact'],
        }
