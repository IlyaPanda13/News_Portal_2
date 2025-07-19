from django.db import models
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст новости")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    def __str__(self):
        return self.title

    def get_short_content(self):
        """Возвращает первые 20 символов текста"""
        return self.content[:20] + '...' if len(self.content) > 20 else self.content

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-pub_date']  # Сортировка по дате (новые сначала)
