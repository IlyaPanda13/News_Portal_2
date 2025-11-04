from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Category, Post
from celery import Celery
from celery.schedules import crontab


@shared_task
def send_new_post_notification(post_id):
    """Асинхронная отправка уведомлений о новой статье подписчикам"""
    try:
        post = Post.objects.get(id=post_id)

        # Получаем все категории статьи
        categories = post.categories.all()

        for category in categories:
            # Получаем всех подписчиков категории
            subscribers = category.subscribers.all()

            for subscriber in subscribers:
                if subscriber.email:
                    subject = f'Новая статья: {post.title}'
                    message = f'''
В категории "{category.name}" опубликована новая статья:

Заголовок: {post.title}
Автор: {post.author.username if post.author else "Неизвестен"} 
Дата публикации: {post.pub_date.strftime("%d.%m.%Y %H:%M")}

{post.content[:200]}...

Перейти к статье: http://127.0.0.1:8000/news/{post.id}/

Вы получили это письмо, потому что подписаны на категорию "{category.name}".
'''
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[subscriber.email],
                    )

        return f"Уведомления отправлены для статьи: {post.title}"

    except Post.DoesNotExist:
        return "Статья не найдена"


app = Celery('newsite')


@shared_task
def send_weekly_digest():
    """Еженедельная рассылка новых статей подписчикам"""

    # Определяем период - последние 7 дней
    week_ago = timezone.now() - timedelta(days=7)

    # Получаем все категории
    categories = Category.objects.all()

    email_count = 0

    for category in categories:
        # Получаем новые статьи за неделю в этой категории
        new_posts = Post.objects.filter(
            categories=category,
            pub_date__gte=week_ago
        ).order_by('-pub_date')

        if new_posts.exists():
            # Получаем всех подписчиков категории
            subscribers = category.subscribers.all()

            for subscriber in subscribers:
                if subscriber.email:
                    subject = f'Еженедельная рассылка: новые статьи в категории "{category.name}"'

                    # Формируем список статей
                    posts_list = ""
                    for post in new_posts:
                        posts_list += f"• {post.title} - http://127.0.0.1:8000/news/{post.id}/\n"

                    message = f'''
Добрый день!

За последнюю неделю в категории "{category.name}" опубликованы новые статьи:

{posts_list}

Всего новых статей: {new_posts.count()}

Приятного чтения!
Команда новостного портала
'''
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[subscriber.email],
                    )
                    email_count += 1

    return f"Еженедельная рассылка отправлена. Писем: {email_count}"