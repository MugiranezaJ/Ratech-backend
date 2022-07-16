from django.contrib import admin

from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'tag_code', 'condition', 'city', 'country', 'price')

# Register your models here.

admin.site.register(Product, ProductAdmin)