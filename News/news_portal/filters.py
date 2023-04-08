from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter, CharFilter
from django.forms import Select, DateTimeInput, TextInput
from .models import Author


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        # required=True,
        label='Заголовок',
        # error_messages={'required': 'Пожалуйста введите название поста!'},
        widget=TextInput(attrs={
            'class': 'border_input'
        })
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все авторы',
        widget=Select(attrs={
            'class': 'border_select'
        })
    )

    time_post = DateTimeFilter(
        field_name='time_post',
        label='Дата',
        lookup_expr='gt',
        widget=DateTimeInput(attrs={
            'type': 'datetime-local',
            'id': 'localdate',
            'name': 'date',
            'value': '2023-03-17T08:00',
            'class': 'border_datetime'
        })
    )
