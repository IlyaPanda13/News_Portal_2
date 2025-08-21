from django import forms
from .models import Post

class NewsSearchForm(forms.Form):
    title = forms.CharField(
        label='Название',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию'})
    )
    author = forms.CharField(
        label='Автор',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по автору'})
    )
    date_after = forms.DateField(
        label='Опубликовано после',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

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