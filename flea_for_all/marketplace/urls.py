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
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:conversation_id>/', views.inbox, name='conversation_detail'),
    path("messages/start/<int:seller_pk>/", views.start_conversation, name="start_conversation"),
    path("messages/start/<int:seller_pk>/", views.start_conversation, name="start_conversation"),
    path("messages/send/<int:pk>/", views.send_widget_message, name="send_widget_message"),
    path("messages/close/<int:pk>/", views.close_chat, name="close_chat"),
    path("messages/<int:pk>/", views.conversation_detail, name="conversation_detail"),
    path("faq/add/", views.add_faq, name="add_faq"),
    path("faq/<int:pk>/edit/", views.edit_faq, name="edit_faq"),
    path("faq/<int:pk>/delete/", views.delete_faq, name="delete_faq"),
    path("stores/<int:pk>/review/add/", views.add_review, name="add_review"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path('category/<str:category_slug>/', views.category_detail, name='category_detail'),
    path("product/add/", views.add_product, name="add_product"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("products/<int:pk>/status/", views.update_product_status, name="update_product_status"),
    path("product/<int:pk>/report/", views.report_product, name="report_product"),
    path("store/<int:pk>/report/", views.report_store, name="report_store"),
    path("verify-email/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('profile/<int:profile_id>/clear-image/<str:image_type>/', views.clear_profile_image, name='clear_profile_image'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('product/<int:product_id>/clear-image/', views.clear_product_image, name='clear_product_image'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('report/<str:report_type>/<int:report_id>/resolve/', views.mark_report_resolved, name='mark_report_resolved'),
    ]
