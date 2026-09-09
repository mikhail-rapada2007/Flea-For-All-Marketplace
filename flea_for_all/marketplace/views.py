from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.db.models import Avg
from .forms import SignUpForm, ProfileEditForm, FAQForm, RatingForm, ProductForm, ProductForm
from .models import Profile, Product, Rating, FAQ, Conversation, Message, Report
from django.contrib.auth.decorators import login_required

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
def inbox(request):
    conversations = request.user.conversations.all()
    return render(request, "marketplace/inbox.html", {"conversations": conversations})

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

def home(request):
    category_filter = request.GET.get("category")
    products = Product.objects.filter(status=Product.Status.AVAILABLE)
    if category_filter:
        products = products.filter(category=category_filter)
    
    return render(request, "marketplace/home.html", {
        "products": products,
        "selected_category": category_filter,
        "categories": Product.Category.choices,
    })

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
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("marketplace:home")
    else:
        form = SignUpForm()
    return render(request, "marketplace/signup.html", {"form": form})

def terms_view(request):
    return render(request, "marketplace/terms.html")

def store_listings(request):
    """Lists every seller's store (Profile) as a browsable directory —
    this is NOT the detailed view of any single store."""
    profiles = Profile.objects.all()
    return render(request, "marketplace/store_listings.html", {"profiles": profiles})

def store_detail(request, pk):
    """Shows one seller's detailed store page: profile header + Listings/FAQ/Reviews tabs."""
    profile = get_object_or_404(Profile, pk=pk)
    products = profile.products.filter(status=Product.Status.AVAILABLE)
    faqs = profile.faqs.all()
    reviews = profile.ratings_received.filter(rating_type=Rating.RatingType.SELLER)
    seller_avg = reviews.aggregate(Avg("score"))["score__avg"]
    rating_form = RatingForm()

    return render(request, "marketplace/store_detail.html", {
        "profile": profile,
        "products": products,
        "faqs": faqs,
        "reviews": reviews,         
        "seller_avg": seller_avg,
        "rating_form": rating_form, 
    })

def product_detail(request, pk):
    """Shows one product's detailed page."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "marketplace/product_detail.html", {"product": product})

def category_detail(request, category_slug):
    products = Product.objects.filter(status=Product.Status.AVAILABLE, category=category_slug)
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
    products = profile.products.filter(status=Product.Status.AVAILABLE)
    faqs = profile.faqs.all()
    reviews = profile.ratings_received.filter(rating_type=Rating.RatingType.SELLER)
    seller_avg = reviews.aggregate(Avg("score"))["score__avg"]
    rating_form = RatingForm()
    product_form = ProductForm()  # <-- Pass product_form for the modal overlay

    return render(request, "marketplace/store_detail.html", {
        "profile": profile,
        "products": products,
        "faqs": faqs,
        "reviews": reviews,         
        "seller_avg": seller_avg,
        "rating_form": rating_form,
        "product_form": product_form,
    })

def store_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    products = profile.products.filter(status=Product.Status.AVAILABLE)
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
        "Report": Report,
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
def add_report(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        reason = request.POST.get("reason")
        details = request.POST.get("details", "")
        Report.objects.create(
            product=product,
            reporter=request.user,
            reason=reason,
            details=details
        )
        return redirect("marketplace:product_detail", pk=product.pk)
    return redirect("marketplace:product_detail", pk=product.pk)

@login_required
def add_store_report(request, pk):
    store = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        reason = request.POST.get("reason")
        details = request.POST.get("details")
        Report.objects.create(
            store=store,
            reporter=request.user,
            reason=reason,
            details=details
        )
        return redirect("marketplace:store_detail", pk=store.pk)
    return redirect("marketplace:store_detail", pk=store.pk)
