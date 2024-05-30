import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import mail_managers
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from news.models import Post, Subscriber, Category
from django.utils.timezone import now
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def weekly_news():
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


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_news,
            trigger=CronTrigger(
                day_of_week='fri', hour="18", minute="00", timezone=settings.TIME_ZONE
            ),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="10", timezone=settings.TIME_ZONE
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
