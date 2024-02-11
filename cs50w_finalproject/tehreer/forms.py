from django import forms
from .models import User, Article

class ArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ("title", "content")

        # remove labels
        labels = {
            "content": "",
            "title": ""
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Title",
                "style": "text-align: center; border: none; border-bottom: 3px solid gray; border-radius: 0px; box-shadow: none; background-color: transparent; font-size: 2rem; font-weight: bold; color: #000000;"
            })                
        }