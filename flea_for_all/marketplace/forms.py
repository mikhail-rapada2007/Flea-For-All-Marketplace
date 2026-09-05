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