from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.news_list, name='news_list'),  # /news/
    path('<int:news_id>/', views.news_detail, name='news_detail'),  # /news/1/
    path('search/', views.news_search, name='news_search'),  # /news/search/

    # Дублирующие пути для совместимости (добавленные из второго фрагмента)
    path('news/', views.news_list, name='news_list'),  # /news/news/
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),  # /news/news/1/
    path('news/search/', views.news_search, name='news_search'),  # /news/news/search/

    # CRUD для новостей
    path('create/', views.news_create, name='news_create'),  # /news/create/
    path('<int:pk>/edit/', views.post_edit, name='news_edit'),  # /news/1/edit/
    path('<int:pk>/delete/', views.post_delete, name='news_delete'),  # /news/1/delete/

    # CRUD для статей
    path('articles/create/', views.article_create, name='article_create'),  # /news/articles/create/
    path('articles/<int:pk>/edit/', views.post_edit, name='article_edit'),  # /news/articles/1/edit/
    path('articles/<int:pk>/delete/', views.post_delete, name='article_delete'),  # /news/articles/1/delete/

    # Профиль
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # /news/profile/edit/
    path('become-author/', views.become_author, name='become_author'),  # /news/become-author/

]