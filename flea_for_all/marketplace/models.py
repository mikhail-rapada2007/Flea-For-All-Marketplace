from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
#User's profile acts as the 'store' page: bio + listings.

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    profile_picture_url = models.URLField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Store"


class Product(models.Model):
#A single listing. Status is controlled by the seller (User).

    class Category(models.TextChoices):
        ELECTRONICS = "ELECTRONICS", "Electronics"
        CLOTHING = "CLOTHING", "Clothing"
        TOYS = "TOYS", "Toys"
        FURNITURE = "FURNITURE", "Furniture"
        BOOKS = "BOOKS", "Books"
        OTHER = "OTHER", "Other"

    class Condition(models.TextChoices):
        NEW = "NEW", "New"
        GOOD = "GOOD", "Good"
        FAIR = "FAIR", "Fair"
        POOR = "POOR", "Poor"

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        RESERVED = "RESERVED", "Reserved"
        SOLD = "SOLD", "Sold"

    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="products")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    condition = models.CharField(max_length=10, choices=Condition.choices, default=Condition.GOOD)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class Report(models.Model):
#Reports are tied to a Product's auto-generated ID.

    class Reason(models.TextChoices):
        FAKE_LISTING = "FAKE", "Fake listing"
        SCAM = "SCAM", "Scam"
        OFFENSIVE = "OFFENSIVE", "Offensive content"
        DUPLICATE = "DUPLICATE", "Duplicate listing"
        OTHER = "OTHER", "Other"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reports")
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reports_filed")
    reason = models.CharField(max_length=20, choices=Reason.choices)
    details = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report on '{self.product.title}' ({self.get_reason_display()})"

class Rating(models.Model):
    class RatingType(models.TextChoices):
        SELLER = "SELLER", "Seller"
        BUYER = "BUYER", "Buyer"

    rated_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="ratings_received")
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings_given")
    rating_type = models.CharField(max_length=10, choices=RatingType.choices)
    score = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_rating_type_display()} rating for {self.rated_profile.user.username}: {self.score}"


class FAQ(models.Model):
    store = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.store.user.username}'s FAQ: {self.question[:50]}"