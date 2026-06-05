#!/usr/bin/env python
"""Test script for creating sample data"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')
django.setup()

from product.models import Category, Product, Review

print("=" * 60)
print("Creating test data...")
print("=" * 60)

# Create categories
print("\n1. Creating categories:")
category1 = Category.objects.create(name="Electronics")
print(f"   Created: {category1.name} (ID: {category1.id})")

category2 = Category.objects.create(name="Clothing")
print(f"   Created: {category2.name} (ID: {category2.id})")

# Create products
print("\n2. Creating products:")
product1 = Product.objects.create(
    title="iPhone 15",
    description="Powerful smartphone",
    price=80000,
    category=category1
)
print(f"   Created: {product1.title} (ID: {product1.id})")

product2 = Product.objects.create(
    title="Samsung Galaxy",
    description="Great smartphone",
    price=70000,
    category=category1
)
print(f"   Created: {product2.title} (ID: {product2.id})")

# Create reviews
print("\n3. Creating reviews:")
review1 = Review.objects.create(
    text="Excellent phone!",
    stars=5,
    product=product1
)
print(f"   Created review for {product1.title} (ID: {review1.id}, stars: {review1.stars})")

review2 = Review.objects.create(
    text="Good product",
    stars=4,
    product=product1
)
print(f"   Created review for {product1.title} (ID: {review2.id}, stars: {review2.stars})")

# Statistics
print("\n" + "=" * 60)
print("STATISTICS:")
print("=" * 60)
print(f"Total categories: {Category.objects.count()}")
print(f"Total products: {Product.objects.count()}")
print(f"Total reviews: {Review.objects.count()}")

print("\n" + "=" * 60)
print("Test data created successfully!")
print("=" * 60)
