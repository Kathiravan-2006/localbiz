from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('category/<str:category>/', views.category, name='category'),
    path('register/', views.register, name='register'),
    path('business/create/', views.create_business, name='create_business'),
    path('business/<int:pk>/', views.business_detail, name='business_detail'),
    path('business/<int:pk>/edit/', views.edit_business, name='edit_business'),
    path('business/<int:pk>/delete/', views.delete_business, name='delete_business'),
    path('review/<int:review_id>/reply/', views.add_review_reply, name='add_review_reply'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/business/<int:pk>/approve/', views.approve_business, name='approve_business'),
    path('dashboard/user/<int:user_id>/toggle-staff/', views.toggle_staff, name='toggle_staff'),
    path('dashboard/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
] 