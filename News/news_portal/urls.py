from django.urls import path
from .views import PostList, PostDetail, PostSearch, CreateNews, UpdateNews, DeleteNews, CreateArticle, upgrade_me

urlpatterns = [
    path('', PostList.as_view(), name='list'),
    path('<int:pk>/', PostDetail.as_view(), name='detail'),
    path('search/', PostSearch.as_view(), name='search'),
    path('create/', CreateNews.as_view(), name='create_news'),
    path('<int:pk>/update/', UpdateNews.as_view(), name='update_news'),
    path('<int:pk>/delete/', DeleteNews.as_view(), name='delete_news'),
    path('article/create/', CreateArticle.as_view(), name='create_article'),
    path('article/<int:pk>/update', UpdateNews.as_view(), name='update_article'),
    path('article/<int:pk>/delete', DeleteNews.as_view(), name='delete_article'),
    path('upgrade/', upgrade_me, name='upgrade_user')
]
