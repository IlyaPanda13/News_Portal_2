from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Добавьте эту строку
    path('', include('news.urls')),
    path('news/', include('news.urls')),
]