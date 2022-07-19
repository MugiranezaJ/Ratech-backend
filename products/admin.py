from django.contrib import admin

from .models import Order, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'tag_code', 'condition', 'city', 'country', 'price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'type', 'status')

# Register your models here.

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)