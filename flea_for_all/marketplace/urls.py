from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("terms/", views.terms_view, name="terms"),
    path("stores/", views.store_listings, name="store_listings"),
    path("stores/<int:pk>/", views.store_detail, name="store_detail"),
    path("messages/", views.inbox, name="inbox"),
    path("messages/start/<int:seller_pk>/", views.start_conversation, name="start_conversation"),
    path("messages/", views.inbox, name="inbox"),
    path("messages/start/<int:seller_pk>/", views.start_conversation, name="start_conversation"),
    path("messages/send/<int:pk>/", views.send_widget_message, name="send_widget_message"),
    path("messages/close/<int:pk>/", views.close_chat, name="close_chat"),
    path("faq/add/", views.add_faq, name="add_faq"),
    path("faq/<int:pk>/edit/", views.edit_faq, name="edit_faq"),
    path("faq/<int:pk>/delete/", views.delete_faq, name="delete_faq"),
    path("stores/<int:pk>/reviesw/add/", views.add_review, name="add_review"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path('category/<str:category_slug>/', views.category_detail, name='category_detail'),
    path("product/add/", views.add_product, name="add_product"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("products/<int:pk>/report/", views.add_report, name="add_report"),
    path("stores/<int:pk>/report/", views.add_store_report, name="add_store_report"),
    path("products/<int:pk>/status/", views.update_product_status, name="update_product_status"),
    ]
