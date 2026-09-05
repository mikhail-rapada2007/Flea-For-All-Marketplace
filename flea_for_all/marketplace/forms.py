from .models import Profile, Product, Rating, FAQ
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "store_name", "bio", "profile_picture_url",
            "city", "province",
            "theme_background_url", "theme_color", "theme_font",
        ]

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer"]