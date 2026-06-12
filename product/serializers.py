from rest_framework import serializers
from django.db.models import Avg
from django.contrib.auth.models import User

from .models import Category, Product, Review, ConfirmationCode


def validate_category_name(value):
    if not value or len(value.strip()) == 0:
        raise serializers.ValidationError("Название категории не может быть пустым.")
    if len(value) < 2:
        raise serializers.ValidationError("Название категории должно содержать минимум 2 символа.")
    if len(value) > 255:
        raise serializers.ValidationError("Название категории не может быть длиннее 255 символов.")
    return value


def validate_product_title(value):
    if not value or len(value.strip()) == 0:
        raise serializers.ValidationError("Название товара не может быть пустым.")
    if len(value) < 3:
        raise serializers.ValidationError("Название товара должно содержать минимум 3 символа.")
    if len(value) > 255:
        raise serializers.ValidationError("Название товара не может быть длиннее 255 символов.")
    return value


def validate_product_price(value):
    if value <= 0:
        raise serializers.ValidationError("Цена товара должна быть больше 0.")
    if value > 999999.99:
        raise serializers.ValidationError("Цена товара не может быть больше 999999.99.")
    return value


def validate_review_text(value):
    if not value or len(value.strip()) == 0:
        raise serializers.ValidationError("Текст отзыва не может быть пустым.")
    if len(value) < 5:
        raise serializers.ValidationError("Текст отзыва должен содержать минимум 5 символов.")
    if len(value) > 5000:
        raise serializers.ValidationError("Текст отзыва не может быть длиннее 5000 символов.")
    return value


def validate_review_stars(value):
    if not isinstance(value, int):
        raise serializers.ValidationError("Количество звёзд должно быть целым числом.")
    if value < 1 or value > 5:
        raise serializers.ValidationError("Количество звёзд должно быть от 1 до 5.")
    return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
    
    def validate_name(self, value):
        return validate_category_name(value)


class CategoryWithCountSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']
    
    def get_products_count(self, obj):
        return obj.products.count()
    
    def validate_name(self, value):
        return validate_category_name(value)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']
    
    def validate_title(self, value):
        return validate_product_title(value)
    
    def validate_description(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Описание товара не может быть пустым.")
        if len(value) < 10:
            raise serializers.ValidationError("Описание товара должно содержать минимум 10 символов.")
        if len(value) > 10000:
            raise serializers.ValidationError("Описание товара не может быть длиннее 10000 символов.")
        return value
    
    def validate_price(self, value):
        return validate_product_price(value)
    
    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError("Категория не может быть пустой.")
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Выбранная категория не существует.")
        return value
    
    def validate(self, data):
        if data.get('title', '').lower().strip() == data.get('description', '').lower().strip():
            raise serializers.ValidationError(
                {"description": "Описание не может быть идентично названию товара."}
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']
    
    def validate_text(self, value):
        return validate_review_text(value)
    
    def validate_stars(self, value):
        return validate_review_stars(value)
    
    def validate_product(self, value):
        if not value:
            raise serializers.ValidationError("Товар не может быть пустым.")
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Выбранный товар не существует.")
        return value
    
    def validate(self, data):
        words = data.get('text', '').strip().split()
        if len(words) < 3:
            raise serializers.ValidationError(
                {"text": "Текст отзыва должен содержать минимум 3 слова."}
            )
        return data


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']
    
    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        return round(avg_rating, 2) if avg_rating else 0
    
    def validate_title(self, value):
        return validate_product_title(value)
    
    def validate_description(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Описание товара не может быть пустым.")
        if len(value) < 10:
            raise serializers.ValidationError("Описание товара должно содержать минимум 10 символов.")
        if len(value) > 10000:
            raise serializers.ValidationError("Описание товара не может быть длиннее 10000 символов.")
        return value
    
    def validate_price(self, value):
        return validate_product_price(value)
    
    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError("Категория не может быть пустой.")
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Выбранная категория не существует.")
        return value

