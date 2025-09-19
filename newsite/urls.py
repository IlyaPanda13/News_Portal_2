from django.contrib import admin
from django.urls import path, include
from news.views import ImmediateYandexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/yandex/immediate/', ImmediateYandexView.as_view(), name='yandex_immediate'),
    path('', include('news.urls')),
]