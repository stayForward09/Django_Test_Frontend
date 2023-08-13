from django import forms
from .models import Category, Type, Article

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = 'category'
    
    class Meta:
        model = Category
        fields = ['name']

class TypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.prefix = 'type'
    
    class Meta:
        model = Type
        fields = ['name', 'category']

class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = 'article'
    
    class Meta:
        model = Article
        fields = ['sn', 'location', 'used', 'model']
