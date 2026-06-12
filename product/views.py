from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, action  
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Category, Product, Review, ConfirmationCode
from .serializers import (
    CategorySerializer,
    CategoryWithCountSerializer,
    ProductSerializer,
    ProductWithReviewsSerializer,
    ReviewSerializer,
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryWithCountSerializer
        return CategorySerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({'error': 'Параметр category_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            category_id = int(category_id)
        except ValueError:
            return Response({'error': 'category_id должно быть числом'}, status=status.HTTP_400_BAD_REQUEST)
        products = Product.objects.filter(category_id=category_id)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ProductWithReviewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer
    pagination_class = StandardResultsSetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_product(self, request):
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({'error': 'Параметр product_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product_id = int(product_id)
        except ValueError:
            return Response({'error': 'product_id должно быть числом'}, status=status.HTTP_400_BAD_REQUEST)
        reviews = Review.objects.filter(product_id=product_id)
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)


class CategoryWithCountListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithCountSerializer
    pagination_class = StandardResultsSetPagination


class ProductWithReviewsListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer
    pagination_class = StandardResultsSetPagination

@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Введите логин и пароль'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Пользователь с таким именем уже существует'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    code = ConfirmationCode.generate_code()
    ConfirmationCode.objects.create(user=user, code=code)

    return Response(
        {
            'message': 'Пользователь создан. Подтвердите аккаунт кодом.',
            'confirmation_code': code
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Введите логин и пароль'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if not user:
        return Response(
            {'error': 'Неверный логин или пароль'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {'error': 'Аккаунт не подтверждён. Введите код из регистрации.'},
            status=status.HTTP_403_FORBIDDEN
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})


@api_view(['POST'])
def confirm_view(request):
    code = request.data.get('code')

    if not code:
        return Response(
            {'error': 'Введите код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        confirmation = ConfirmationCode.objects.get(code=code)
    except ConfirmationCode.DoesNotExist:
        return Response(
            {'error': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = confirmation.user
    user.is_active = True
    user.save()

    confirmation.delete() 

    return Response({'message': 'Аккаунт успешно подтверждён! Теперь можете войти.'})