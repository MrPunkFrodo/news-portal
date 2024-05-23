from django import forms
from .models import Post, Category

class NewsSearchForm(forms.Form):
    title = forms.CharField(label='Заголовок новости', required=False)
    postCategory = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', required=False)