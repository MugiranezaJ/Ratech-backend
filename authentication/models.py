from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.

class UserProfile(models.Model):
    class RoleType(models.TextChoices):
        ADMIN = 'admin'
        SELLER = 'seller'
        EDITOR = 'editor'
    uuid = models.CharField(
        primary_key=True,
        unique=True,
        default=uuid4,
        max_length=100)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="abstract_user_model")
    resident_city = models.CharField(max_length=225, blank=True)
    resident_country = models.CharField(max_length=225, blank=True)
    phone = models.CharField(max_length=225, blank=True)
    profile_image = models.TextField(default="", blank=True)
    is_verified = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(blank=False, default=False)
    role = models.CharField(choices=RoleType.choices, max_length = 255, blank=False)
    gender = models.CharField(max_length=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    # def __str__(self):
    #     return "{} -{}".format(self.username, self.email)