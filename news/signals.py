from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from .models import Post, Subscriber
from django.db.models.signals import m2m_changed


@receiver(m2m_changed, sender=Post.postCategory.through)
def news_created_sub(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.postCategory.all()
        subscribers = Subscriber.objects.filter(category__in=categories).select_related('user')

        post_url = reverse('detail', kwargs={'pk': instance.pk})
        full_url = f'http://127.0.0.1:8000{post_url}'

        for subscriber in subscribers:
            send_mail(
                subject=f'New news Post',
                message=f'Читать полностью: {instance.title}\n{full_url}',
                from_email='no-reply@example.com',
                recipient_list=[subscriber.user.email],
            )
