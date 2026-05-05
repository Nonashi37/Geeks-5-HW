from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ReviewSerializer, 
    ProductReviewSerializer
)

# --- CATEGORY ---

@api_view(['GET'])
def category_list_api_view(request):
    # Let the DB count the products for us
    categories = Category.objects.annotate(products_count=Count('product'))
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_detail_api_view(request, id):
    # Detail views usually don't need the count, but you can add it if needed
    category = get_object_or_404(Category, id=id)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


# --- PRODUCT ---

@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_reviews_list_api_view(request):
    """
    New endpoint: /api/v1/products/reviews/
    Returns products with their reviews and average stars.
    """
    # .prefetch_related('reviews') prevents the "N+1" query problem!
    products = Product.objects.prefetch_related('reviews').annotate(
        average_rating=Avg('reviews__stars')
    )
    serializer = ProductReviewSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail_api_view(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


# --- REVIEW ---

@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    review = get_object_or_404(Review, id=id)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)