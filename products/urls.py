from django.urls import path

from .views import CheckView, OrderView, ProductAddView, ProductSearchView

urlpatterns = [
    path('add', ProductAddView.as_view(), name="product_add"),
    path('search', ProductSearchView.as_view(), name="product_search"),
    path('check', CheckView.as_view(), name='check'),
    path('order', OrderView.as_view(), name='order')
]