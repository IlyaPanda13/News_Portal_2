from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Отправляет приветственное письмо при регистрации нового пользователя"""

    if created:  # Отправляем только при создании нового пользователя
        subject = 'Добро пожаловать на Новостной портал!'
        message = f'''
Здравствуйте, {instance.username}!

Добро пожаловать на наш Новостной портал!

Теперь вы можете:
• Читать новости и статьи
• Подписываться на интересующие категории
• Получать уведомления о новых публикациях
• Комментировать материалы (если станете автором)

Для начала работы посетите наш сайт:
http://127.0.0.1:8000/

С уважением,
Команда Новостного портала
'''
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
        )