import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsite.settings')

app = Celery('newsite')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Настройка периодических задач
app.conf.beat_schedule = {
    'send-weekly-digest-every-monday-8am': {
        'task': 'news.tasks.send_weekly_digest',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Каждый понедельник в 8:00
    },
}

app.autodiscover_tasks()