from django.urls import path
from .views import PostsList, detail

urlpatterns = [
    path('news/', PostsList.as_view(), name='news_list'),
    path('news/<int:pk>', detail, name='detail'),

]
