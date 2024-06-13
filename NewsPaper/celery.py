import os

from celery.schedules import crontab

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.send_weekly_news',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}