#!/usr/bin/env python
"""
Скрипт для тестирования CRUD операций API
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')
django.setup()

from product.models import Category, Product, Review

print("="*60)
print("ТЕСТИРОВАНИЕ API ENDPOINTS")
print("="*60)

# 1. Создание категории
print("\n1️⃣  СОЗДАНИЕ КАТЕГОРИИ:")
category = Category.objects.create(name="Электроника")
print(f"   ✓ Создана категория: {category.name} (ID: {category.id})")

category2 = Category.objects.create(name="Одежда")
print(f"   ✓ Создана категория: {category2.name} (ID: {category2.id})")

# 2. Создание товаров
print("\n2️⃣  СОЗДАНИЕ ТОВАРОВ:")
product = Product.objects.create(
    title="iPhone 15",
    description="Мощный смартфон",
    price=80000,
    category=category
)
print(f"   ✓ Создан товар: {product.title} (ID: {product.id})")

product2 = Product.objects.create(
    title="Samsung Galaxy",
    description="Отличный смартфон",
    price=70000,
    category=category
)
print(f"   ✓ Создан товар: {product2.title} (ID: {product2.id})")

# 3. Создание отзывов
print("\n3️⃣  СОЗДАНИЕ ОТЗЫВОВ:")
review = Review.objects.create(
    text="Отличный телефон, рекомендую!",
    stars=5,
    product=product
)
print(f"   ✓ Создан отзыв к товару '{product.title}' (ID: {review.id}, звезды: {review.stars})")

review2 = Review.objects.create(
    text="Хороший товар",
    stars=4,
    product=product
)
print(f"   ✓ Создан отзыв к товару '{product.title}' (ID: {review2.id}, звезды: {review2.stars})")

# 4. Вывод статистики
print("\n📊 СТАТИСТИКА:")
print(f"   • Всего категорий: {Category.objects.count()}")
print(f"   • Всего товаров: {Product.objects.count()}")
print(f"   • Всего отзывов: {Review.objects.count()}")

print("\n" + "="*60)
print("ГОТОВО! Теперь тестируй эти endpoint'ы:")
print("="*60)
print("\n📍 GET /api/v1/categories/")
print(f"   Должны увидеть {Category.objects.count()} категорий")

print("\n📍 GET /api/v1/products/")
print(f"   Должны увидеть {Product.objects.count()} товаров")

print("\n📍 GET /api/v1/reviews/")
print(f"   Должны увидеть {Review.objects.count()} отзывов")

print("\n📍 GET /api/v1/categories/1/")
print(f"   Должна вернуть категорию 'Электроника'")

print("\n📍 POST /api/v1/products/")
print("   Можно создать новый товар (JSON):")
print("   {\"title\": \"Samsung\", \"description\": \"desc\", \"price\": 50000, \"category\": 1}")

print("\n📍 PUT /api/v1/products/1/")
print("   Можно изменить товар (полное обновление)")

print("\n📍 PATCH /api/v1/products/1/")
print("   Можно изменить отдельное поле товара")

print("\n📍 DELETE /api/v1/reviews/1/")
print("   Можно удалить отзыв")

print("\n" + "="*60)
