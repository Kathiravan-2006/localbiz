from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Business, Review, UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 'category', 'address', 'phone', 'website', 'description', 'services')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'services': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Business Name',
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewReplyForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('reply',)
        widgets = {
            'reply': forms.Textarea(attrs={'rows': 3}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4})) 