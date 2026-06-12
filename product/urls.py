from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_root import api_root

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'reviews', views.ReviewViewSet, basename='review')

urlpatterns = [
    path('', api_root, name='api-root'),
    path('products/reviews/', views.ProductWithReviewsListView.as_view(), name='product-reviews-list'),
    path('', include(router.urls)),
    path('users/register/', views.register_view),
    path('users/login/', views.login_view),
    path('users/confirm/', views.confirm_view),
]