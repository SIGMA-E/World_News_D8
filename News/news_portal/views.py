from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import CreateNewsForm, UpdateNewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    model = Post
    ordering = 'time_post'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):  # создаем форму для поиска по модели Post
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset  # помещаем форму в переменную
        if not self.request.user.is_staff:
            context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_staff:
            context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearch(LoginRequiredMixin, PostList):  # представление формы поиска поста
    template_name = 'search.html'


class CreateNews(PermissionRequiredMixin, CreateView):  # представление формы для создания новости
    form_class = CreateNewsForm
    model = Post
    template_name = 'create.html'
    permission_required = 'news_portal.add_post'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type_post = 'nw'
        return super().form_valid(form)


class CreateArticle(PermissionRequiredMixin, CreateView):  # представление для создания статьи
    form_class = CreateNewsForm
    model = Post
    template_name = 'create.html'
    permission_required = 'news_portal.add_post'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type_post = 'ar'
        return super().form_valid(form)


class UpdateNews(PermissionRequiredMixin, UpdateView):  # представление для редактирования новости/статьи
    form_class = UpdateNewsForm
    model = Post
    template_name = 'update.html'
    permission_required = 'news_portal.change_post'


class DeleteNews(LoginRequiredMixin, DeleteView):  # представление для удаления новости/статьи
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('list')


@login_required
def upgrade_me(request):  # кнопка стать автором
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/news')
