from django import forms
from .models import User, Article
from django.contrib.auth.forms import UserCreationForm



class SignupForm(forms.ModelForm):

    password2 = forms.CharField()
    

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'bio', 'profile_picture']


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 4:
            raise forms.ValidationError("Password must be at least 4 characters long.")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if len(password2) < 4:
            raise forms.ValidationError("Password must be at least 4 characters long.")
        return password2
    
    
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