from django.urls import path
from .views import (
    CategoryListAPIView,
    CategoryDetailAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ReviewListAPIView,
    ReviewDetailAPIView,
)

urlpatterns = [
    path('api/v1/categories/', CategoryListAPIView.as_view()),
    path('api/v1/categories/<int:id>/', CategoryDetailAPIView.as_view()),

    path('api/v1/products/', ProductListAPIView.as_view()),
    path('api/v1/products/<int:id>/', ProductDetailAPIView.as_view()),

    path('api/v1/reviews/', ReviewListAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', ReviewDetailAPIView.as_view()),
]