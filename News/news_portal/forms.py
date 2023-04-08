from django.forms import (ModelForm, CharField, TextInput, Textarea,
                          ModelChoiceField, ModelMultipleChoiceField,
                          Select, SelectMultiple)
from .models import Post, Author, Category
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CreateNewsForm(ModelForm):  # форма для создания новости/статьи
    title = CharField(
        max_length=255,
        label='Заголовок',
        widget=TextInput(attrs={
            'class': 'border_input'
        })
    )

    text_post = CharField(
        label="Текст поста",
        widget=Textarea(attrs={
            'class': 'text_post'
        })
    )

    author = ModelChoiceField(
        to_field_name='user',
        label='Автор',
        queryset=Author.objects.all(),
        empty_label='Выберите автора',
        widget=Select(attrs={
            'class': 'border_select'
        })
    )

    category = ModelMultipleChoiceField(
        to_field_name='name_category',
        label='Категория',
        queryset=Category.objects.all(),
        widget=SelectMultiple(attrs={
            'class': 'border_select'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'text_post', 'author', 'category']

    def clean(self):  # валидатор формы создания новости/статьи
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        query_list = [i['title'] for i in Post.objects.all().values('title')]  # список заголовков
        if title in query_list:  # если заголовок уже существует в списке
            raise ValidationError({
                'title': 'Такой заголовок уже существует!',
            })

        text_post = cleaned_data.get('text_post')
        if text_post is not None and len(text_post) < 100:  # если текст поста меньше 100 символов
            print('Ошибка')
            raise ValidationError({
                'text_post': 'Содержание поста слишком краткое, меньше 100 символов!!!'
            })
        return cleaned_data


class UpdateNewsForm(ModelForm):  # форма для редактирования новости (не стал наследоваться из-за стилей)
    title = CharField(
        max_length=255,
        label='Заголовок',
        widget=TextInput(attrs={
            'class': 'border_input'
        })
    )

    text_post = CharField(
        label="Текст поста",
        widget=Textarea(attrs={
            'class': 'text_post'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'text_post']

    def clean(self):  # валидатор формы редактора новости
        cleaned_data = super().clean()
        text_post = cleaned_data.get('text_post')
        if text_post is not None and len(text_post) < 100:  # если текст поста меньше 100 символов
            raise ValidationError({
                'text_post': 'Содержание поста слишком краткое, меньше 100 символов!!!'
            })
        return cleaned_data


class BasicSignupForm(SignupForm):  # добавление user в группу common после успешной регистрации
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
