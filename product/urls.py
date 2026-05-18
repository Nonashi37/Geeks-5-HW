from django.urls import path
from . import views  # Senior tip: Import the whole module to keep this clean!

urlpatterns = [
    # Auth Endpoints (CBVs need .as_view())
    path('api/v1/users/register/', views.RegisterAPIView.as_view()),
    path('api/v1/users/confirm/', views.ConfirmAPIView.as_view()),
    path('api/v1/users/login/', views.AuthorizationAPIView.as_view()),

    # Category Endpoints
    path('api/v1/categories/', views.category_list_api_view),
    path('api/v1/categories/<int:id>/', views.category_detail_api_view),

    # Product Endpoints
    path('api/v1/products/', views.product_list_api_view),
    path('api/v1/products/reviews/', views.product_reviews_list_api_view),  # Specific path stays on top!
    path('api/v1/products/<int:id>/', views.product_detail_api_view),

    # Review Endpoints
    path('api/v1/reviews/', views.review_list_api_view),
    path('api/v1/reviews/<int:id>/', views.review_detail_api_view),
]