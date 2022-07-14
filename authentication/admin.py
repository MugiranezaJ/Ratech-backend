from django.contrib import admin
from .models import Otp, PasswordReset, UserProfile

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

class OtpAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'code', 'email', 'is_verified', 'is_delivered')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PasswordReset)
admin.site.register(Otp, OtpAdmin)