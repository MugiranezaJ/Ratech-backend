from django.urls import path

from .views import ProductAddView, ProductSearchView

urlpatterns = [
    path('add', ProductAddView.as_view(), name="product_add"),
    path('search', ProductSearchView.as_view(), name="product_search")
]