from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import Post, Subscriber, Category
from NewsPaper import settings
from django.urls import reverse


# @shared_task
# def hello():
#     time.sleep(3)
#     print("Hello, world!")
#
# class MyTasks(View):
#     def get(self,request):
#         hello.delay()
#
#         return HttpResponse('hello!')

@shared_task
def send_note(pk):
    posts = Post.objects.get(pk=pk)
    categories = set(post.postCategory.values_list('name', flat=True) for post in posts)
    subscribers = set(User.objects.filter(subscriber__category__name__in=categories))

    post_url = reverse('detail', kwargs={pk})
    full_url = f'http://127.0.0.1:8000{post_url}'

    for subscriber in subscribers:
        send_mail(
            subject=f'New news Post {Post.title}',
            message=f'Читать полностью: {Post.title}\n{full_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=set[subscriber.user.email],
        )


@shared_task
def send_weekly_news():
    last_week = now() - timedelta(days=7)

    posts = Post.objects.filter(date_created__gte=last_week)

    categories = set(post.postCategory.values_list('name', flat=True) for post in posts)
    subscribers = set(User.objects.filter(subscriber__category__name__in=categories))

    for sub in subscribers:
        sub_cat = sub.subscriber.values_list('category__postcategory', flat=True)
        posts_cat_sub = posts.filter(postCategory__postcategory__in=sub_cat)

        message = f"Привет, {sub.username}!\n\nНовости за неделю:\n\n"
        for post in posts_cat_sub:
            message += f"{post.title}\n"
            message += f"http://127.0.0.1{post.get_absolute_url()}\n\n"

        send_mail(
            'Weekly Newsletter',
            message,
            'from@example.com',
            [sub.email],
            fail_silently=False,
        )
