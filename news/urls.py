from django.urls import path
from .views import PostsList, PostDetail, NewsSearch, NewsCreate, PostEdit, PostDelete, ArticlesCreate

urlpatterns = [
    path('news/', PostsList.as_view(), name='news_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='detail'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostEdit.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),

]
