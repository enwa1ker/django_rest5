from django.http import JsonResponse


def api_root(request):
    link = request.build_absolute_uri
    return JsonResponse({
        'categories': link('categories/'),
        'products': link('products/'),
        'reviews': link('reviews/'),
    })
