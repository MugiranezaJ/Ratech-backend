from django.contrib import admin
from .models import UserProfile

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "resident_country",
        "phone",
        "profile_image",
        "is_active",
        "role",
        "created_at",
        "modified_at",
        "is_verified")


admin.site.register(UserProfile, UserProfileAdmin)