#!/bin/bash
# Примеры curl команд для тестирования валидации API

BASE_URL="http://localhost:8000/api/v1"

echo "=== TESTING CATEGORIES API ==="

# 1. Успешное создание категории
echo -e "\n1. CREATE VALID CATEGORY"
curl -X POST "$BASE_URL/categories/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Электроника"}'

# 2. Ошибка: пустое имя категории
echo -e "\n\n2. CREATE CATEGORY - EMPTY NAME (ERROR)"
curl -X POST "$BASE_URL/categories/" \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'

# 3. Ошибка: слишком короткое имя
echo -e "\n\n3. CREATE CATEGORY - TOO SHORT (ERROR)"
curl -X POST "$BASE_URL/categories/" \
  -H "Content-Type: application/json" \
  -d '{"name": "А"}'

# 4. Получить список категорий
echo -e "\n\n4. GET CATEGORIES LIST"
curl -X GET "$BASE_URL/categories/"

# 5. Получить категории с пагинацией
echo -e "\n\n5. GET CATEGORIES WITH PAGINATION"
curl -X GET "$BASE_URL/categories/?page=1&page_size=5"

echo -e "\n\n=== TESTING PRODUCTS API ==="

# 6. Успешное создание товара
echo -e "\n6. CREATE VALID PRODUCT"
curl -X POST "$BASE_URL/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 15 Pro",
    "description": "Флагманский смартфон Apple с процессором A17 Pro, камерой 48MP и поддержкой 5G",
    "price": 999.99,
    "category": 1
  }'

# 7. Ошибка: пустое название товара
echo -e "\n\n7. CREATE PRODUCT - EMPTY TITLE (ERROR)"
curl -X POST "$BASE_URL/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "",
    "description": "Флагманский смартфон Apple с процессором A17 Pro, камерой 48MP и поддержкой 5G",
    "price": 999.99,
    "category": 1
  }'

# 8. Ошибка: слишком короткое описание
echo -e "\n\n8. CREATE PRODUCT - SHORT DESCRIPTION (ERROR)"
curl -X POST "$BASE_URL/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 15",
    "description": "Смартфон",
    "price": 999.99,
    "category": 1
  }'

# 9. Ошибка: отрицательная цена
echo -e "\n\n9. CREATE PRODUCT - NEGATIVE PRICE (ERROR)"
curl -X POST "$BASE_URL/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 15",
    "description": "Флагманский смартфон Apple с процессором A17 Pro",
    "price": -100,
    "category": 1
  }'

# 10. Ошибка: несуществующая категория
echo -e "\n\n10. CREATE PRODUCT - INVALID CATEGORY (ERROR)"
curl -X POST "$BASE_URL/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 15",
    "description": "Флагманский смартфон Apple с процессором A17 Pro",
    "price": 999.99,
    "category": 9999
  }'

# 11. Получить товары определённой категории
echo -e "\n\n11. GET PRODUCTS BY CATEGORY"
curl -X GET "$BASE_URL/products/by_category/?category_id=1"

# 12. Ошибка: отсутствует параметр category_id
echo -e "\n\n12. GET PRODUCTS BY CATEGORY - MISSING PARAM (ERROR)"
curl -X GET "$BASE_URL/products/by_category/"

# 13. Получить список всех товаров
echo -e "\n\n13. GET PRODUCTS LIST"
curl -X GET "$BASE_URL/products/"

echo -e "\n\n=== TESTING REVIEWS API ==="

# 14. Успешное создание отзыва
echo -e "\n14. CREATE VALID REVIEW"
curl -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Отличный товар, очень доволен покупкой и рекомендую всем!",
    "stars": 5,
    "product": 1
  }'

# 15. Ошибка: пустой текст отзыва
echo -e "\n\n15. CREATE REVIEW - EMPTY TEXT (ERROR)"
curl -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "",
    "stars": 5,
    "product": 1
  }'

# 16. Ошибка: слишком короткий текст
echo -e "\n\n16. CREATE REVIEW - TOO SHORT TEXT (ERROR)"
curl -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Хор",
    "stars": 5,
    "product": 1
  }'

# 17. Ошибка: недостаточно слов
echo -e "\n\n17. CREATE REVIEW - TOO FEW WORDS (ERROR)"
curl -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Хороший товар",
    "stars": 5,
    "product": 1
  }'

# 18. Ошибка: слишком мало звёзд
echo -e "\n\n18. CREATE REVIEW - STARS TOO LOW (ERROR)"
curl -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Отличный товар, очень доволен покупкой!",
    "stars": 0,
    "product": 1
  }'

# 19. Ошибка: слишком много звёзд
echo -e "\n\n19. CREATE REVIEW - STARS TOO HIGH (ERROR)"
curl -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Отличный товар, очень доволен покупкой!",
    "stars": 6,
    "product": 1
  }'

# 20. Ошибка: несуществующий товар
echo -e "\n\n20. CREATE REVIEW - INVALID PRODUCT (ERROR)"
curl -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Отличный товар, очень доволен покупкой!",
    "stars": 5,
    "product": 9999
  }'

# 21. Получить отзывы определённого товара
echo -e "\n\n21. GET REVIEWS BY PRODUCT"
curl -X GET "$BASE_URL/reviews/by_product/?product_id=1"

# 22. Ошибка: отсутствует параметр product_id
echo -e "\n\n22. GET REVIEWS BY PRODUCT - MISSING PARAM (ERROR)"
curl -X GET "$BASE_URL/reviews/by_product/"

# 23. Получить список всех отзывов
echo -e "\n\n23. GET REVIEWS LIST"
curl -X GET "$BASE_URL/reviews/"

echo -e "\n\n=== TESTING ADVANCED API ==="

# 24. Получить товары со всеми отзывами и рейтингом
echo -e "\n24. GET PRODUCTS WITH REVIEWS AND RATING"
curl -X GET "$BASE_URL/products_with_reviews/"

echo -e "\n\n=== ALL TESTS COMPLETED ==="
