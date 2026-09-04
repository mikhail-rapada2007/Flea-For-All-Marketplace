from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from .models import Profile, Product


def home(request):
#THIS IS  A PLACEHOLDER HOMEPAGE — it lists available products. Replace or expand this part as views get built out.
    products = Product.objects.filter(status=Product.Status.AVAILABLE)
    return render(request, "marketplace/home.html", {"products": products})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # every new account gets a Profile immediately
            login(request, user)
            return redirect("marketplace:home")
    else:
        form = SignUpForm()
    return render(request, "marketplace/signup.html", {"form": form})

def terms_view(request):
    return render(request, "marketplace/terms.html")