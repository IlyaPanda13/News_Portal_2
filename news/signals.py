# news/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.conf import settings


@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    """
    Автоматически добавляет нового пользователя в группу 'common' при создании.
    """
    if created:  # Если пользователь только что создан
        try:
            # Получаем группу 'common'
            common_group = Group.objects.get(name=settings.COMMON_GROUP_NAME)
            # Добавляем пользователя в группу
            instance.groups.add(common_group)
            # Сохраняем пользователя (изменения в M2M сохраняются автоматически, но для ясности)
            instance.save()
        except Group.DoesNotExist:
            # Группа не существует, можно записать в лог или проигнорировать
            pass