from django import forms
from .models import User, Article
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    # email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    # bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    # profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'bio', 'profile_picture')


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