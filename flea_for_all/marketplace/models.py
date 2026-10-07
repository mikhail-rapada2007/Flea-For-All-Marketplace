from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Profile(models.Model):
    # User's profile acts as the 'store' page: bio + listings.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profiles/avatars/", blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    store_name = models.CharField(max_length=100, blank=True)
    theme_background = models.ImageField(upload_to="profiles/backgrounds/", blank=True, null=True)
    theme_color = models.CharField(max_length=7, blank=True, help_text="Hex color, e.g. #524336")

    class ThemeFont(models.TextChoices):
        DEFAULT = "DEFAULT", "Default"
        SHRIKHAND = "SHRIKHAND", "Shrikhand"
        POPPINS = "POPPINS", "Poppins"
        PLAYFAIR = "PLAYFAIR", "Playfair Display"
        COMFORTAA = "COMFORTAA", "Comfortaa"
        PACIFICO = "PACIFICO", "Pacifico"

    theme_font = models.CharField(max_length=20, choices=ThemeFont.choices, default=ThemeFont.DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)

    class LayoutStyle(models.TextChoices):
        TABS = "TABS", "Classic Tabs"
        SIDEBAR = "SIDEBAR", "Sidebar Split (Q&A + Reviews Right)"
        FEED = "FEED", "Featured & Review Ticker"
        BAZAAR = "BAZAAR", "Bazaar Showcase (Store Info Left)"

    layout_style = models.CharField(
        max_length=20,
        choices=LayoutStyle.choices,
        default=LayoutStyle.TABS
    )

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
    image = models.ImageField(upload_to="products/%Y/%m/", blank=True, null=True)
    condition = models.CharField(max_length=10, choices=Condition.choices, default=Condition.GOOD)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("marketplace:product_detail", kwargs={"pk": self.id})

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class BaseReport(models.Model):
    class Reason(models.TextChoices):
        FAKE_LISTING = "FAKE", "Fake listing"
        SCAM = "SCAM", "Scam"
        OFFENSIVE = "OFFENSIVE", "Offensive content"
        DUPLICATE = "DUPLICATE", "Duplicate listing"
        OTHER = "OTHER", "Other"

    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_filed")
    reason = models.CharField(max_length=20, choices=Reason.choices)
    details = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class ProductReport(BaseReport):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reports")
    class Meta(BaseReport.Meta):
        pass
    def __str__(self):
        return f"Report on '{self.product.title}' ({self.get_reason_display()})"

class StoreReport(BaseReport):
    store = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reports")
    class Meta(BaseReport.Meta):
        pass
    def __str__(self):
        return f"Report on '{self.store.user.username}' ({self.get_reason_display()})"

class Rating(models.Model):
    class RatingType(models.TextChoices):
        SELLER = "SELLER", "Seller"
        BUYER = "BUYER", "Buyer"

    rated_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="ratings_received")
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings_given")
    rating_type = models.CharField(max_length=10, choices=RatingType.choices)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
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

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def get_other_user(self, current_user):
        """Returns the participant that is not the current user."""
        return self.participants.exclude(pk=current_user.pk).first()

    def __str__(self):
        return f"Conversation #{self.pk}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sent_at"]

    def __str__(self):
        return f"Message from {self.sender.username} at {self.sent_at}"

@receiver(post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(post_delete, sender=Profile)
def auto_delete_profile_images_on_delete(sender, instance, **kwargs):
    if instance.profile_picture and os.path.isfile(instance.profile_picture.path):
        os.remove(instance.profile_picture.path)
    if instance.theme_background and os.path.isfile(instance.theme_background.path):
        os.remove(instance.theme_background.path)