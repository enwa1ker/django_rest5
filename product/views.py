from rest_framework import viewsets, generics

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    CategoryWithCountSerializer,
    ProductSerializer,
    ProductWithReviewsSerializer,
    ReviewSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_serializer_class(self):
        # Use CategoryWithCountSerializer for list view
        if self.action == 'list':
            return CategoryWithCountSerializer
        return CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductWithReviewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CategoryWithCountListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithCountSerializer


class ProductWithReviewsListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer
