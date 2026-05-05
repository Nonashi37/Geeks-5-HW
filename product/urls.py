from django.urls import path
from .views import (
    category_list_api_view,
    category_detail_api_view,
    product_list_api_view,
    product_detail_api_view,
    product_reviews_list_api_view,  # <--- Don't forget this import!
    review_list_api_view,
    review_detail_api_view,
)

urlpatterns = [
    # Category endpoints
    path('api/v1/categories/', category_list_api_view),
    path('api/v1/categories/<int:id>/', category_detail_api_view),

    # Product endpoints
    path('api/v1/products/', product_list_api_view),
    
    # NEW: Specific path for reviews goes ABOVE the ID path
    path('api/v1/products/reviews/', product_reviews_list_api_view),
    
    path('api/v1/products/<int:id>/', product_detail_api_view),

    # Review endpoints
    path('api/v1/reviews/', review_list_api_view),
    path('api/v1/reviews/<int:id>/', review_detail_api_view),
]