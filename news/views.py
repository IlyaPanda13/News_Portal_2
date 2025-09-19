from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import HttpResponse
from .models import Post
from .forms import PostForm, NewsSearchForm, UserEditForm
from django.views import View
from django.shortcuts import redirect
from allauth.socialaccount.providers.yandex.views import YandexOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


def is_author(user):
    """Проверяет, находится ли пользователь в группе authors"""
    return user.groups.filter(name='authors').exists()


def news_list(request):
    news_items = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(news_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'page_obj': page_obj})


def news_detail(request, news_id):
    news = get_object_or_404(Post, id=news_id)  # Используем id, а не pk
    return render(request, 'news/news_detail.html', {'news': news})


def news_search(request):
    form = NewsSearchForm(request.GET or None)
    news_items = Post.objects.all().order_by('-pub_date')

    if form.is_valid():
        title = form.cleaned_data.get('title')
        author = form.cleaned_data.get('author')
        date_after = form.cleaned_data.get('date_after')

        if title:
            news_items = news_items.filter(title__icontains=title)
        if author:
            news_items = news_items.filter(author__username__icontains=author)
        if date_after:
            news_items = news_items.filter(pub_date__gte=date_after)

    paginator = Paginator(news_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_search.html', {
        'form': form,
        'page_obj': page_obj,
        'search_performed': bool(request.GET)
    })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('news_list')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'news/profile_edit.html', {'form': form})


@login_required
def news_create(request):
    return post_create(request, 'news')


@login_required
def article_create(request):
    return post_create(request, 'article')


@login_required
def post_create(request, post_type):
    # Проверяем права через группу authors
    if not is_author(request.user):
        messages.error(request, 'Только авторы могут создавать публикации!')
        return redirect('news_list')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.post_type = post_type
            post.save()
            messages.success(request, 'Публикация успешно создана!')
            return redirect('news_list')
    else:
        initial = {'post_type': post_type}
        form = PostForm(initial=initial)

    title = 'Создание новости' if post_type == 'news' else 'Создание статьи'
    return render(request, 'news/post_form.html', {'form': form, 'title': title})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Двойная проверка: группа authors + автор публикации
    if not is_author(request.user) or post.author != request.user:
        messages.error(request, 'Вы можете редактировать только свои публикации!')
        return redirect('news_list')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Публикация успешно обновлена!')
            return redirect('news_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'news/post_form.html', {
        'form': form,
        'title': f'Редактирование: {post.title}'
    })


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Двойная проверка: группа authors + автор публикации
    if not is_author(request.user) or post.author != request.user:
        messages.error(request, 'Вы можете удалять только свои публикации!')
        return redirect('news_list')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Публикация успешно удалена!')
        return redirect('news_list')

    return render(request, 'news/post_confirm_delete.html', {'post': post})


@login_required
def become_author(request):
    """Функция для запроса статуса автора"""
    if request.method == 'POST':
        try:
            # Получаем обе группы
            authors_group = Group.objects.get(name='authors')
            common_group = Group.objects.get(name='common')

            # Добавляем пользователя в обе группы
            request.user.groups.add(authors_group, common_group)

            messages.success(request, 'Теперь вы автор! Можете создавать публикации.')
            return redirect('news_list')
        except Group.DoesNotExist:
            messages.error(request, 'Группы не найдены. Обратитесь к администратору.')
            return redirect('news_list')

    return render(request, 'news/become_author.html')


# Тестовая функция для проверки
def test_view(request):
    return HttpResponse("Test page - no redirects")


class ImmediateYandexView(View):
    """Немедленный HTTP 302 редирект на Yandex"""

    def get(self, request):
        try:
            # Создаем адаптер
            adapter = YandexOAuth2Adapter(request)

            # Получаем URL для авторизации используя правильные методы
            # Используем authorize_url вместо get_authorize_url
            login_url = adapter.authorize_url

            # Получаем client_id и secret через объект app
            app = adapter.get_provider().app
            client_id = app.client_id
            client_secret = app.secret

            # Создаем OAuth2 клиент
            client = OAuth2Client(
                request,
                client_id,
                client_secret,
                adapter.access_token_method,
                adapter.access_token_url,
                adapter.get_callback_url(request),
                adapter.get_scope()
            )

            # Получаем полный URL для редиректа
            redirect_url = client.get_redirect_url(login_url)
            return redirect(redirect_url)

        except Exception as e:
            # В случае ошибки просто редиректим на стандартный URL авторизации
            login_url = adapter.get_provider().get_login_url(request)
            return redirect(login_url)