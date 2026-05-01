from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer


# CATEGORY


@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    data = CategorySerializer(categories, many=True).data
    return Response(data)


@api_view(['GET'])
def category_detail_api_view(request, id):
    category = get_object_or_404(Category, id=id)
    data = CategorySerializer(category).data
    return Response(data)



# PRODUCT


@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductSerializer(products, many=True).data
    return Response(data)


@api_view(['GET'])
def product_detail_api_view(request, id):
    product = get_object_or_404(Product, id=id)
    data = ProductSerializer(product).data
    return Response(data)



# REVIEW


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(reviews, many=True).data
    return Response(data)


@api_view(['GET'])
def review_detail_api_view(request, id):
    review = get_object_or_404(Review, id=id)
    data = ReviewSerializer(review).data
    return Response(data)