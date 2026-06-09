from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from product.models import Category, Product, Review


class CategoryValidationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/categories/'
    
    def test_create_category_valid(self):
        data = {'name': 'Электроника'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Электроника')
    
    def test_create_category_empty_name(self):
        data = {'name': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
    
    def test_create_category_too_short(self):
        data = {'name': 'А'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
    
    def test_create_category_too_long(self):
        data = {'name': 'A' * 300}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)


class ProductValidationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/products/'
        self.category = Category.objects.create(name='Электроника')
    
    def test_create_product_valid(self):
        data = {
            'title': 'Air Jordan 1 Retro Low OG Travis Scott',
            'description': 'Легендарные кроссовки сотрудничества Travis Scott и Jordan Brand',
            'price': 1299.99,
            'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_product_empty_title(self):
        data = {
            'title': '',
            'description': 'Хорошее описание товара',
            'price': 100,
            'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_create_product_short_title(self):
        data = {
            'title': 'AB',
            'description': 'Хорошее описание товара',
            'price': 100,
            'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_short_description(self):
        data = {
            'title': 'Товар',
            'description': 'Коротко',
            'price': 100,
            'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_invalid_price(self):
        data = {
            'title': 'Товар',
            'description': 'Хорошее описание товара',
            'price': -10,
            'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)
    
    def test_create_product_zero_price(self):
        data = {
            'title': 'Товар',
            'description': 'Хорошее описание товара',
            'price': 0,
            'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_invalid_category(self):
        data = {
            'title': 'Товар',
            'description': 'Хорошее описание товара',
            'price': 100,
            'category': 9999
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_identical_title_description(self):
        title_desc = 'Это один и тот же текст для названия и описания'
        data = {
            'title': title_desc,
            'description': title_desc,
            'price': 100,
            'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewValidationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/reviews/'
        self.category = Category.objects.create(name='Электроника')
        self.product = Product.objects.create(
            title='Air Jordan 1 Retro Low OG Travis Scott',
            description='Легендарные кроссовки сотрудничества Travis Scott и Jordan Brand',
            price=1299.99,
            category=self.category
        )
    
    def test_create_review_valid(self):
        data = {
            'text': 'Прекрасные кроссовки, качество на высоте!',
            'stars': 5,
            'product': self.product.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_review_empty_text(self):
        data = {
            'text': '',
            'stars': 5,
            'product': self.product.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('text', response.data)
    
    def test_create_review_short_text(self):
        data = {
            'text': 'Хор',
            'stars': 5,
            'product': self.product.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_review_too_few_words(self):
        data = {
            'text': 'Хороший товар',
            'stars': 5,
            'product': self.product.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_review_invalid_stars_too_low(self):
        data = {
            'text': 'Отличный товар, очень доволен покупкой!',
            'stars': 0,
            'product': self.product.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('stars', response.data)
    
    def test_create_review_invalid_stars_too_high(self):
        data = {
            'text': 'Отличный товар, очень доволен покупкой!',
            'stars': 6,
            'product': self.product.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_review_invalid_stars_string(self):
        data = {
            'text': 'Отличный товар, очень доволен покупкой!',
            'stars': 'пять',
            'product': self.product.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_review_invalid_product(self):
        data = {
            'text': 'Отличный товар, очень доволен покупкой!',
            'stars': 5,
            'product': 9999
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PaginationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        for i in range(15):
            Category.objects.create(name=f'Категория {i+1}')
    
    def test_default_pagination(self):
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['count'], 15)
        self.assertIsNotNone(response.data['next'])
    
    def test_custom_page_size(self):
        response = self.client.get('/api/v1/categories/?page_size=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
    
    def test_second_page(self):
        response = self.client.get('/api/v1/categories/?page=2&page_size=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)


class FilterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Электроника')
        self.product = Product.objects.create(
            title='Air Jordan 1 Retro Low OG Travis Scott',
            description='Легендарные кроссовки сотрудничества Travis Scott и Jordan Brand',
            price=1299.99,
            category=self.category
        )
        self.review = Review.objects.create(
            text='Прекрасные кроссовки, качество на высоте!',
            stars=5,
            product=self.product
        )
    
    def test_filter_products_by_category(self):
        response = self.client.get(
            f'/api/v1/products/by_category/?category_id={self.category.id}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_products_by_category_invalid_param(self):
        response = self.client.get('/api/v1/products/by_category/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_filter_reviews_by_product(self):
        response = self.client.get(
            f'/api/v1/reviews/by_product/?product_id={self.product.id}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_reviews_by_product_invalid_param(self):
        response = self.client.get('/api/v1/reviews/by_product/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
