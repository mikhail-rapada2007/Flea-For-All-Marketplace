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
            "store_name", "bio", "profile_picture",
            "city", "province",
            'theme_background',
        ]

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer"]

class RatingForm(forms.ModelForm):
    score = forms.ChoiceField(
        choices=[(i, f"{i}" + ("" if i > 1 else "")) for i in range(5, 0, -1)],
        widget=forms.RadioSelect(attrs={'class': 'rating-stars-input'})
    )

    class Meta:
        model = Rating
        fields = ['score', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'category', 'condition', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'store_name',
            'city',
            'province',
            'bio',
            'profile_picture',
            'theme_background',
            'theme_color',
            'theme_font',
        ]
        widgets = {
            'store_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your store's display name"}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Province'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell buyers about your store...'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'theme_background': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'theme_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color', 'style': 'height: 42px; padding: 4px;'}),
            'theme_font': forms.Select(attrs={'class': 'form-select'}),
        }