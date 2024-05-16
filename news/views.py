from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = 'date_created'
    template_name = 'posts_page.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.now()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context


def detail(request, pk):
    post = Post.objects.get(pk__iexact=pk)
    return render(request, "details.html", context={'post': post.text})

