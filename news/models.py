# news/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django import forms


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    subscribers = models.ManyToManyField(User, through='Subscription', related_name='subscribed_categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    subscribed_at = models.DateTimeField(default=timezone.now, verbose_name="Дата подписки")

    class Meta:
        unique_together = ('user', 'category')  # Одна подписка на категорию для пользователя
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name="Публикация")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return f"{self.post.title} - {self.category.name}"

    class Meta:
        verbose_name = "Категория публикации"
        verbose_name_plural = "Категории публикаций"


class Post(models.Model):
    POST_TYPES = [
        ('news', 'Новость'),
        ('article', 'Статья'),
    ]

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    pub_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='news', verbose_name="Тип")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Автор"
    )
    # Добавляем связь с категориями
    categories = models.ManyToManyField(Category, through=PostCategory, verbose_name="Категории")

    def __str__(self):
        return f"{self.get_post_type_display()}: {self.title}"

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-pub_date']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'post_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'post_type': 'Тип публикации',
        }


from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    """Создает группы при миграциях"""
    Group.objects.get_or_create(name='common')
    Group.objects.get_or_create(name='authors')