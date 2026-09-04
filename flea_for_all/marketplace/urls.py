from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("terms/", views.terms_view, name="terms"),
    path("stores/", views.store_listings, name="store_listings"),
]