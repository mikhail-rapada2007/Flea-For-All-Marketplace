import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.db.models import Avg
from .forms import SignUpForm, ProfileEditForm, FAQForm, RatingForm, ProductForm, ProductForm, ProductReportForm, StoreReportForm
from .models import Profile, Product, Rating, FAQ, Conversation, Message, ProductReport, StoreReport
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST

def home(request):
    category_filter = request.GET.get("category")
    products = Product.objects.all()
    if category_filter:
        products = products.filter(category=category_filter)
    
    return render(request, "marketplace/home.html", {
        "products": products,
        "selected_category": category_filter,
        "categories": Product.Category.choices,
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("marketplace:store_detail", pk=profile.pk)
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, "marketplace/edit_profile.html", {"form": form})

@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Message.objects.create(conversation=conversation, sender=request.user, content=content)
        return redirect("marketplace:conversation_detail", pk=pk)
    return render(request, "marketplace/conversation_detail.html", {"conversation": conversation})

@login_required
def start_conversation(request, seller_pk):
    seller_profile = get_object_or_404(Profile, pk=seller_pk)
    if seller_profile.user == request.user:
        return redirect("marketplace:store_detail", pk=seller_pk)

    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(participants=seller_profile.user).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, seller_profile.user)

    open_ids = request.session.get("open_conversation_ids", [])
    if conversation.pk not in open_ids:
        open_ids.append(conversation.pk)
    request.session["open_conversation_ids"] = open_ids

    return redirect(request.META.get("HTTP_REFERER", "marketplace:home"))


@login_required
def send_widget_message(request, pk):
    if request.method == "POST":
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        content = request.POST.get("content", "").strip()
        if content:
            Message.objects.create(conversation=conversation, sender=request.user, content=content)
    return redirect(request.META.get("HTTP_REFERER", "marketplace:home"))


@login_required
def close_chat(request, pk):
    open_ids = request.session.get("open_conversation_ids", [])
    if pk in open_ids:
        open_ids.remove(pk)
    request.session["open_conversation_ids"] = open_ids
    return redirect(request.META.get("HTTP_REFERER", "marketplace:home"))

@login_required
def inbox(request, conversation_id=None):
    # Fetch all user conversations ordered by created_at
    conversations = list(Conversation.objects.filter(participants=request.user).order_by('-created_at'))

    # Attach other participant safely
    for convo in conversations:
        convo.other_person = convo.get_other_user(request.user)

    active_conversation = None
    if conversation_id:
        active_conversation = get_object_or_404(Conversation, pk=conversation_id, participants=request.user)
        active_conversation.other_person = active_conversation.get_other_user(request.user)

    # Handle sending messages directly in the active chat view
    if request.method == "POST" and active_conversation:
        content = request.POST.get("content", "").strip()
        if content:
            Message.objects.create(
                conversation=active_conversation,
                sender=request.user,
                content=content
            )
            return redirect('marketplace:conversation_detail', conversation_id=active_conversation.pk)

    return render(request, "marketplace/inbox.html", {
        "conversations": conversations,
        "active_conversation": active_conversation,
    })

@login_required
def add_faq(request):
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.store = request.user.profile
            faq.save()
            return redirect("marketplace:store_detail", pk=request.user.profile.pk)
    else:
        form = FAQForm()
    return render(request, "marketplace/faq_form.html", {"form": form})


@login_required
def edit_faq(request, pk):
    faq = get_object_or_404(FAQ, pk=pk, store=request.user.profile)
    if request.method == "POST":
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            return redirect("marketplace:store_detail", pk=request.user.profile.pk)
    else:
        form = FAQForm(instance=faq)
    return render(request, "marketplace/faq_form.html", {"form": form})


@login_required
def delete_faq(request, pk):
    faq = get_object_or_404(FAQ, pk=pk, store=request.user.profile)
    if request.method == "POST":
        faq.delete()
        return redirect("marketplace:store_detail", pk=request.user.profile.pk)
    return render(request, "marketplace/faq_confirm_delete.html", {"faq": faq})

@login_required
def add_review(request, pk):
    store_profile = get_object_or_404(Profile, pk=pk)
    
    if store_profile.user == request.user:
        return redirect("marketplace:store_detail", pk=pk)

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.rated_profile = store_profile
            review.rated_by = request.user
            review.rating_type = Rating.RatingType.SELLER
            review.save()
            return redirect("marketplace:store_detail", pk=pk)
    else:
        form = RatingForm()
        
    return render(request, "marketplace/review_form.html", {"form": form, "store": store_profile})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # blocked from logging in until verified
            user.save()
            Profile.objects.create(user=user)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verify_url = request.build_absolute_uri(
                reverse("marketplace:verify_email", kwargs={"uidb64": uid, "token": token})
            )

            send_mail(
                subject="Verify your Flea For All account",
                message=f"Hi {user.username},\n\nClick the link below to verify your email and activate your account:\n\n{verify_url}\n\nIf you didn't sign up, ignore this email.",
                from_email=None,
                recipient_list=[user.email],
            )

            return render(request, "marketplace/check_email.html", {"email": user.email})
    else:
        form = SignUpForm()
    return render(request, "marketplace/signup.html", {"form": form})

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        user.profile.is_verified = True
        user.profile.save()
        login(request, user)
        messages.success(request, "Your email has been verified! Welcome to Flea For All.")
        return redirect("marketplace:home")
    else:
        messages.error(request, "This verification link is invalid or has expired.")
        return redirect("login")

def terms_view(request):
    return render(request, "marketplace/terms.html")

def store_listings(request):
    """Lists every seller's store (Profile) as a browsable directory —
    this is NOT the detailed view of any single store."""
    profiles = Profile.objects.all()
    return render(request, "marketplace/store_listings.html", {"profiles": profiles})

def product_detail(request, pk):
    """Shows one product's detailed page."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "marketplace/product_detail.html", {"product": product})

def category_detail(request, category_slug):
    products = Product.objects.all()
    return render(request, "marketplace/category_detail.html", {
        "products": products,
        "selected_category": category_slug,
        "categories": Product.Category.choices,
    })

  
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.profile
            product.save()
            return redirect('marketplace:store_detail', pk=request.user.profile.pk)
    return redirect('marketplace:store_detail', pk=request.user.profile.pk)


def store_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    products = profile.products.all()
    faqs = profile.faqs.all()
    reviews = profile.ratings_received.filter(rating_type=Rating.RatingType.SELLER)
    seller_avg = reviews.aggregate(Avg("score"))["score__avg"]

    return render(request, "marketplace/store_detail.html", {
        "profile": profile,
        "products": products,
        "faqs": faqs,
        "reviews": reviews,         
        "seller_avg": seller_avg,
        "rating_form": RatingForm(),
        "product_form": ProductForm(),
        "profile_form": ProfileEditForm(instance=profile),  
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("marketplace:store_detail", pk=profile.pk)
        else:
            print("Profile Edit Errors:", form.errors)  
            return redirect("marketplace:store_detail", pk=profile.pk)
    else:
        form = ProfileEditForm(instance=profile)
    return redirect("marketplace:store_detail", pk=profile.pk)

@login_required
def update_product_status(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user.profile)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in dict(Product.Status.choices):
            product.status = status
            product.save()
    return redirect("marketplace:product_detail", pk=product.pk)

@login_required
def report_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.product = product
            report.reporter = request.user
            report.save()
            messages.success(request, "Report submitted. Thank you.")
            return redirect("marketplace:product_detail", pk=product.pk)
    else:
        form = ProductReportForm()
    return render(request, "marketplace/report_product.html", {"form": form, "product": product})


@login_required
def report_store(request, pk):
    store = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        form = StoreReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.store = store
            report.reporter = request.user
            report.save()
            messages.success(request, "Report submitted. Thank you.")
            return redirect("marketplace:store_detail", pk=store.pk)
    else:
        form = StoreReportForm()
    return render(request, "marketplace/report_store.html", {"form": form, "store": store})




@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to view the admin dashboard.")
        return redirect('marketplace:home')

    all_profiles = Profile.objects.all().order_by('-created_at')
    all_products = Product.objects.all().order_by('-created_at')

    # Unresolved reports sort first automatically: False (0) sorts before True (1)
    product_reports = ProductReport.objects.all().order_by('is_resolved', '-created_at')
    store_reports = StoreReport.objects.all().order_by('is_resolved', '-created_at')

    stats = {
        'total_users': User.objects.count(),
        'total_listings': Product.objects.count(),
        'available_count': Product.objects.filter(status=Product.Status.AVAILABLE).count(),
        'reserved_count': Product.objects.filter(status=Product.Status.RESERVED).count(),
        'sold_count': Product.objects.filter(status=Product.Status.SOLD).count(),
        'pending_reports': product_reports.filter(is_resolved=False).count() + store_reports.filter(is_resolved=False).count(),
    }

    return render(request, 'marketplace/admin_dashboard.html', {
        'profiles': all_profiles,
        'products': all_products,
        'product_reports': product_reports,
        'store_reports': store_reports,
        'stats': stats,
    })

@require_POST
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_staff or request.user.profile == product.seller:
        product.delete()
        messages.success(request, f"Listing '{product.title}' was successfully deleted.")
    else:
        messages.error(request, "You do not have permission to delete this listing.")
        
    if request.user.is_staff:
        return redirect('marketplace:admin_dashboard')
    else:

        return redirect('marketplace:home') 
    
@require_POST
@login_required
def clear_profile_image(request, profile_id, image_type):
    if not request.user.is_staff:
        messages.error(request, "Only admins can remove profile images.")
        return redirect('marketplace:home') 
        
    profile = get_object_or_404(Profile, id=profile_id)
    
    if image_type == 'avatar' and profile.profile_picture:
        profile.profile_picture.delete(save=True)
        messages.success(request, f"Removed profile picture for {profile.user.username}.")
        
    elif image_type == 'background' and profile.theme_background:
        profile.theme_background.delete(save=True)
        messages.success(request, f"Removed theme background for {profile.user.username}.")
    else:
        messages.warning(request, "No image found to remove.")
        
    return redirect('marketplace:admin_dashboard')

@require_POST
@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to delete users.")
        return redirect('marketplace:home')

    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('marketplace:admin_dashboard')

    if target_user.is_staff:
        messages.error(request, "You cannot delete another staff account from here.")
        return redirect('marketplace:admin_dashboard')

    username = target_user.username
    target_user.delete()
    messages.success(request, f"User '{username}' and all their data was permanently deleted.")
    return redirect('marketplace:admin_dashboard')

@require_POST
@login_required
def clear_product_image(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "Only admins can remove product images.")
        return redirect('marketplace:home')

    product = get_object_or_404(Product, id=product_id)
    if product.image:
        product.image.delete(save=True)
        messages.success(request, f"Removed image for '{product.title}'.")
    else:
        messages.warning(request, "No image found to remove.")

    return redirect('marketplace:admin_dashboard')

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not (request.user.is_staff or request.user.profile == product.seller):
        messages.error(request, "You do not have permission to edit this listing.")
        return redirect('marketplace:product_detail', pk=product.pk)

    if request.method == "POST":
        old_image = product.image
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if 'image' in request.FILES and old_image and os.path.isfile(old_image.path):
                os.remove(old_image.path)
            form.save()
            messages.success(request, f"'{product.title}' was updated.")
            return redirect('marketplace:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, "marketplace/edit_product.html", {"form": form, "product": product})

@require_POST
@login_required
def mark_report_resolved(request, report_type, report_id):
    if not request.user.is_staff:
        messages.error(request, "Only admins can resolve reports.")
        return redirect('marketplace:home')

    if report_type == 'product':
        report = get_object_or_404(ProductReport, id=report_id)
    elif report_type == 'store':
        report = get_object_or_404(StoreReport, id=report_id)
    else:
        messages.error(request, "Invalid report type.")
        return redirect('marketplace:admin_dashboard')

    report.is_resolved = True
    report.save()
    messages.success(request, "Report marked as resolved.")
    return redirect('marketplace:admin_dashboard')