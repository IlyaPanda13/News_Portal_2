from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.news_list, name='news_list'),  # Список всех публикаций
    path('<int:news_id>/', views.news_detail, name='news_detail'),  # Детальная страница
    path('search/', views.news_search, name='news_search'),  # Поиск

    # CRUD для новостей
    path('create/', views.news_create, name='news_create'),  # Создание новости
    path('<int:pk>/edit/', views.post_edit, name='news_edit'),  # Редактирование
    path('<int:pk>/delete/', views.post_delete, name='news_delete'),  # Удаление

    # CRUD для статей
    path('articles/create/', views.article_create, name='article_create'),  # Создание статьи
    path('articles/<int:pk>/edit/', views.post_edit, name='article_edit'),  # Редактирование
    path('articles/<int:pk>/delete/', views.post_delete, name='article_delete'),  # Удаление
]