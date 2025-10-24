import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Category, Post

logger = logging.getLogger(__name__)


def send_weekly_digest():
    """Отправляет еженедельную рассылку новых статей подписчикам"""
    logger.info("Starting weekly digest job...")

    # Определяем период - последние 7 дней
    week_ago = timezone.now() - timedelta(days=7)

    # Получаем все категории
    categories = Category.objects.all()
    logger.info(f"Found {categories.count()} categories")

    email_count = 0

    for category in categories:
        # Получаем новые статьи за неделю в этой категории
        new_posts = Post.objects.filter(
            categories=category,
            pub_date__gte=week_ago
        ).order_by('-pub_date')

        logger.info(f"Category '{category.name}': {new_posts.count()} new posts")

        if new_posts.exists():
            # Получаем всех подписчиков категории
            subscribers = category.subscribers.all()
            logger.info(f"Category '{category.name}': {subscribers.count()} subscribers")

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
                    try:
                        send_mail(
                            subject=subject,
                            message=message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[subscriber.email],
                        )
                        email_count += 1
                        logger.info(f"Email sent to {subscriber.email}")
                    except Exception as e:
                        logger.error(f"Failed to send email to {subscriber.email}: {e}")

    logger.info(f"Weekly digest completed. Sent {email_count} emails.")


def send_new_post_notification(post):
    """Отправляет уведомление о новой статье подписчикам категорий"""

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