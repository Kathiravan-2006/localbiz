from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Check if the is_staff filter is applied in the URL
        if 'is_staff__exact' in request.GET:
            is_staff_value = request.GET['is_staff__exact']
            # Djongo has issues with boolean filtering in admin, filter in Python
            if is_staff_value == '1':
                return [user for user in queryset.all() if user.is_staff]
            elif is_staff_value == '0':
                 return [user for user in queryset.all() if not user.is_staff]

        return queryset

# Unregister the default UserAdmin if it was registered implicitly
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)
