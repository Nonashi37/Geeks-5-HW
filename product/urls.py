from django.urls import path
from . import views

urlpatterns = [
    # Auth Layout
    path('api/v1/users/register/', views.RegisterAPIView.as_view()),
    path('api/v1/users/confirm/', views.ConfirmAPIView.as_view()),
    path('api/v1/users/login/', views.AuthorizationAPIView.as_view()),

    # Category Layout
    path('api/v1/categories/', views.CategoryListAPIView.as_view()),
    path('api/v1/categories/<int:id>/', views.CategoryDetailAPIView.as_view()),

    # Product Layout
    path('api/v1/products/', views.ProductListAPIView.as_view()),
    path('api/v1/products/reviews/', views.ProductReviewsListAPIView.as_view()),  # Must sit above <int:id>
    path('api/v1/products/<int:id>/', views.ProductDetailAPIView.as_view()),

    # Review Layout
    path('api/v1/reviews/', views.ReviewListAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),
]