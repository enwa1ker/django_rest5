from django.urls import path

from .page_views import (
    CategoryDetail,
    CategoryList,
    HomePage,
    ProductDetail,
    ProductList,
    ReviewDetail,
    ReviewList,
)

urlpatterns = [
    path('', HomePage.as_view(), name='page-home'),
    path('categories/', CategoryList.as_view(), name='page-category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='page-category-detail'),
    path('products/', ProductList.as_view(), name='page-product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='page-product-detail'),
    path('reviews/', ReviewList.as_view(), name='page-review-list'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='page-review-detail'),
]
