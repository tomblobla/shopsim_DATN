from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Tag, Category, Order
from .serializers import ProductSerializer, TagSerializer, CategorySerializer


def shop(request, category_slug=None):
    categories = None
    products = None

    if (category_slug != None):
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(
            is_available=True).order_by('created_date')[:16]

    productsSerializer = ProductSerializer(products, many=True)

    productsSerializer = ProductSerializer(
        products, many=True)

    tagSerializer = TagSerializer(
        Tag.objects.all(), many=True)

    categorySerializer = CategorySerializer(Category.objects.all(), many=True)

    context = {
        "tags": tagSerializer.data,
        "products": productsSerializer.data,
        "categories": categorySerializer.data,
    }

    return render(request, 'shop.html', context)

