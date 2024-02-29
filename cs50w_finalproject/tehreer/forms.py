from django import forms
from .models import User, Article
from django.contrib.auth.forms import AuthenticationForm
from django.utils import html
from django_quill.quill import Quill, QuillParseError



class SignupForm(forms.ModelForm):
    '''
    Form based on User model with additional password2 field for confirmation
    '''

    password2 = forms.CharField()
    

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'bio', 'profile_picture']

        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        self.validate_password_match(password, password2)

    def validate_password_match(self, password, password2):
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match.")

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 4:
            raise forms.ValidationError("Password must be at least 4 characters long.")
        return password
    
    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if len(password2) < 4:
            raise forms.ValidationError("Password must be at least 4 characters long.")
        return password2
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not all(char.isalpha() for char in first_name):
            raise forms.ValidationError("First name can't have numbers or special characters.")
        return first_name.capitalize()
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not all(char.isalpha() for char in last_name):
            raise forms.ValidationError("Last name can't have numbers or special characters.")
        return last_name.capitalize()
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()


class SigninForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']


    
class ArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ["title", "content"]

        # remove labels
        labels = {
            "content": "",
            "title": ""
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "article-form-title centered",
                "placeholder": "Title",
            }),
        }

    def clean_content(self):
        content = (self.cleaned_data.get('content'))
        try:
            print(f"Quillified content: {Quill(content).plain}")
            print(Quill(content).plain)
        except QuillParseError:
            print(f"Quillified content: parse error")

        return content