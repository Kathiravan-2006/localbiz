from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from .models import Business, Review, UserProfile, User
from .forms import (
    UserRegistrationForm, BusinessForm, ReviewForm,
    ReviewReplyForm, UserProfileForm, ContactForm
)
from django.http import HttpResponseForbidden

def home(request):
    # Fetch all businesses and perform filtering/annotation/sorting in Python
    all_businesses = Business.objects.all()
    
    # Filter approved businesses in Python
    approved_businesses = [b for b in all_businesses if getattr(b, 'is_approved', False)]
    
    # Annotate with average rating in Python
    for business in approved_businesses:
        reviews = Review.objects.filter(business=business)
        business.avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        
    # Sort by average rating (descending) and take the top 4 in Python
    featured_businesses = sorted(approved_businesses, key=lambda x: x.avg_rating, reverse=True)[:4]
    
    # Get all unique categories
    categories = Business.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'home.html', {
        'featured_businesses': featured_businesses,
        'categories': categories,
    })

def search(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    rating_filter = request.GET.get('rating', '')
    
    # Fetch all approved businesses and perform filtering/annotation in Python due to Djongo compatibility issues
    all_businesses = Business.objects.all()
    
    # Filter approved businesses first in Python
    businesses = [b for b in all_businesses if getattr(b, 'is_approved', False)]
    
    # Apply text query filter in Python
    if query:
        businesses = [b for b in businesses if 
                      query.lower() in getattr(b, 'name', '').lower() or 
                      query.lower() in getattr(b, 'category', '').lower() or 
                      query.lower() in getattr(b, 'description', '').lower() or 
                      query.lower() in getattr(b, 'address', '').lower()]
                      
    # Apply category filter in Python
    if category:
        businesses = [b for b in businesses if getattr(b, 'category', '') == category]
        
    # Calculate average rating and apply rating filter in Python
    businesses_with_ratings = []
    for business in businesses:
        reviews = Review.objects.filter(business=business)
        # Calculate average rating, default to 0 if no reviews
        avg_rating_agg = reviews.aggregate(Avg('rating'))['rating__avg']
        business.avg_rating = avg_rating_agg if avg_rating_agg is not None else 0
        businesses_with_ratings.append(business)
        
    # Apply rating filter
    if rating_filter:
        try:
            min_rating = float(rating_filter)
            businesses_with_ratings = [b for b in businesses_with_ratings if b.avg_rating >= min_rating]
        except ValueError:
            pass # Ignore invalid rating filter
            
    # Sort by average rating (descending) as a default order, can be adjusted
    businesses_with_ratings.sort(key=lambda x: x.avg_rating, reverse=True)

    # Get all categories for the filter dropdown (this query might work with Djongo)
    categories = Business.objects.values_list('category', flat=True).distinct()
    
    # Paginate the results in Python
    paginator = Paginator(businesses_with_ratings, 9)
    page = request.GET.get('page')
    businesses_page = paginator.get_page(page)
    
    return render(request, 'search_results.html', {
        'businesses': businesses_page,
        'query': query,
        'categories': categories,
        'selected_category': category,
        'selected_rating': rating_filter
    })

def category(request, category):
    # Fetch all businesses and perform filtering/annotation/sorting in Python due to Djongo compatibility issues
    all_businesses = Business.objects.all()

    # Filter by category and approved status in Python
    businesses = [b for b in all_businesses if getattr(b, 'category', '') == category and getattr(b, 'is_approved', False)]

    # Annotate with average rating in Python
    businesses_with_ratings = []
    for business in businesses:
        reviews = Review.objects.filter(business=business)
        # Calculate average rating, default to 0 if no reviews
        avg_rating_agg = reviews.aggregate(Avg('rating'))['rating__avg']
        business.avg_rating = avg_rating_agg if avg_rating_agg is not None else 0
        businesses_with_ratings.append(business)

    # Sort by average rating (descending) in Python
    businesses_with_ratings.sort(key=lambda x: x.avg_rating, reverse=True)

    # Create a list for star rating display for each business
    for business in businesses_with_ratings:
        business.star_range = range(int(round(business.avg_rating)))

    # Paginate the results in Python
    paginator = Paginator(businesses_with_ratings, 9)
    page = request.GET.get('page')
    businesses_page = paginator.get_page(page)

    return render(request, 'category.html', {
        'businesses': businesses_page,
        'category': category,
        'total_reviews': sum(b.reviews.count() for b in businesses) # Pass total reviews for percentage calculation in template
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_business(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            messages.success(request, 'Business listing created successfully!')
            return redirect('business_detail', pk=business.pk)
    else:
        form = BusinessForm()
    return render(request, 'create_business.html', {'form': form})

@login_required
def edit_business(request, pk):
    business = get_object_or_404(Business, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = BusinessForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, 'Business listing updated successfully!')
            return redirect('business_detail', pk=business.pk)
    else:
        form = BusinessForm(instance=business)
    return render(request, 'edit_business.html', {'form': form, 'business': business})

@login_required
def delete_business(request, pk):
    business = get_object_or_404(Business, pk=pk, owner=request.user)
    if request.method == 'POST':
        business.delete()
        messages.success(request, 'Business listing deleted successfully!')
        return redirect('home')
    return render(request, 'delete_business.html', {'business': business})

def business_detail(request, pk):
    business = get_object_or_404(Business, pk=pk)
    reviews = business.reviews.all().order_by('-created_at')
    
    # Calculate average rating for the business
    avg_rating_agg = reviews.aggregate(Avg('rating'))['rating__avg']
    business.avg_rating = avg_rating_agg if avg_rating_agg is not None else 0
    
    # Create a list for star rating display
    # Round the average rating and create a list of that many items
    star_range = range(int(round(business.avg_rating)))
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            # Check if user has already reviewed this business
            if Review.objects.filter(business=business, user=request.user).exists():
                messages.warning(request, 'You have already reviewed this business.')
            else:
                Review.objects.create(
                    business=business,
                    user=request.user,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Review added successfully!')
            return redirect('business_detail', pk=pk)
    
    # Calculate review counts for each rating level
    rating_counts = {}
    total_reviews = reviews.count()
    for i in range(1, 6):
        count = reviews.filter(rating=i).count()
        rating_counts[i] = {
            'count': count,
            'percentage': (count / total_reviews * 100) if total_reviews > 0 else 0
        }
        
    # Prepare rating data as a list for easier template access
    rating_data_list = []
    for i in range(5, 0, -1): # Iterate from 5 down to 1
        rating_data_list.append({
            'rating': i,
            'count': rating_counts.get(i, {}).get('count', 0),
            'percentage': rating_counts.get(i, {}).get('percentage', 0)
        })
        
    context = {
        'business': business,
        'reviews': reviews,
        'rating_counts': rating_counts, # Keep original for reference if needed elsewhere
        'total_reviews': total_reviews, # Pass total reviews for percentage calculation in template
        'rating_data_list': rating_data_list, # New list for template iteration
        'star_range': star_range,
    }
    return render(request, 'business_detail.html', context)

def add_review_reply(request, review_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    review = get_object_or_404(Review, pk=review_id)
    
    if request.user != review.business.owner:
        return HttpResponseForbidden()
        
    if request.method == 'POST':
        reply = request.POST.get('reply')
        if reply:
            review.reply = reply
            review.save()
            
    return redirect('business_detail', pk=review.business.pk)

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_businesses = Business.objects.filter(owner=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'profile.html', {
        'form': form,
        'user_businesses': user_businesses,
        'user_reviews': user_reviews
    })

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you would typically send an email
            messages.success(request, 'Message sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def faq(request):
    return render(request, 'faq.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get status filter
    status = request.GET.get('status', 'all')
    
    # Fetch all businesses and filter in Python due to Djongo compatibility issues
    all_businesses = list(Business.objects.all())
    
    if status == 'pending':
        # A business is pending if is_approved is False or the field is missing
        businesses = [b for b in all_businesses if not getattr(b, 'is_approved', False)]
    elif status == 'approved':
        # A business is approved if is_approved is True
        businesses = [b for b in all_businesses if getattr(b, 'is_approved', False)]
    else:
        # 'all' status or any other status gets all businesses
        businesses = all_businesses
    
    # Order businesses by creation date in Python
    businesses.sort(key=lambda x: x.created_at, reverse=True)
    
    # Get users and reviews (these queries seem to be working)
    users = User.objects.all().order_by('-date_joined')
    reviews = Review.objects.all().order_by('-created_at')
    
    return render(request, 'admin_dashboard.html', {
        'businesses': businesses,
        'users': users,
        'reviews': reviews
    })

@login_required
def approve_business(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    business = get_object_or_404(Business, pk=pk)
    
    if request.method == 'POST':
        business.is_approved = True
        business.save()
        messages.success(request, f'Business "{business.name}" has been approved.')
    
    return redirect('admin_dashboard')

@login_required
def toggle_staff(request, user_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        user.is_staff = not user.is_staff
        user.save()
        messages.success(request, f'User "{user.username}" staff status has been updated.')
    
    return redirect('admin_dashboard')

@login_required
def delete_review(request, review_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    review = get_object_or_404(Review, pk=review_id)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review has been deleted.')
    
    return redirect('admin_dashboard')
