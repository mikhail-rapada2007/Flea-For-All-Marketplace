from django.contrib import admin
from .models import Profile, Product, Report, Rating, FAQ

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "province", "is_verified", "created_at")
    list_filter = ("is_verified", "province")
    search_fields = ("user__username", "user__email", "city", "province")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "category", "price", "status", "condition", "created_at")
    list_filter = ("status", "condition", "category")
    search_fields = ("title", "description", "seller__user__username")
    list_editable = ("status",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("get_target", "reason", "reporter", "is_resolved", "created_at")
    list_filter = ("reason", "is_resolved")
    search_fields = ("product__title", "store__user__username")
    list_editable = ("is_resolved",)

    def get_target(self, obj):
        if obj.product:
            return f"Product: {obj.product.title}"
        elif obj.store:
            return f"Store: {obj.store.user.username}"
        return "-"
    get_target.short_description = "Target"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("rated_profile", "rated_by", "rating_type", "score", "created_at")
    list_filter = ("rating_type", "score")
    search_fields = ("rated_profile__user__username", "rated_by__username", "comment")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("store", "question", "created_at")
    list_filter = ("store",)
    search_fields = ("question", "answer", "store__user__username")