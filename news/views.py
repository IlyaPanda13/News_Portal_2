from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm, NewsSearchForm


def news_list(request):
    news_items = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(news_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'page_obj': page_obj})


def news_detail(request, news_id):
    news = get_object_or_404(Post, id=news_id)
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
def news_create(request):
    return post_create(request, 'news')


@login_required
def article_create(request):
    return post_create(request, 'article')


@login_required
def post_create(request, post_type):
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

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Публикация успешно удалена!')
        return redirect('news_list')

    return render(request, 'news/post_confirm_delete.html', {'post': post})