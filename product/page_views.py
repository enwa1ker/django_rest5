from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Product, Review


class HomePage(TemplateView):
    template_name = 'product/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories_count'] = Category.objects.count()
        ctx['products_count'] = Product.objects.count()
        ctx['reviews_count'] = Review.objects.count()
        return ctx


class CategoryList(ListView):
    model = Category
    template_name = 'product/category_list.html'
    context_object_name = 'categories'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'product/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['products'] = self.object.products.all()
        return ctx


class ProductList(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.select_related('category')


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.select_related('category')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['reviews'] = self.object.reviews.all()
        return ctx


class ReviewList(ListView):
    model = Review
    template_name = 'product/review_list.html'
    context_object_name = 'reviews'
    queryset = Review.objects.select_related('product')


class ReviewDetail(DetailView):
    model = Review
    template_name = 'product/review_detail.html'
    context_object_name = 'review'

    def get_queryset(self):
        return Review.objects.select_related('product')
