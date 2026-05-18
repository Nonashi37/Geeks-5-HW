from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Category, Product, Review, UserConfirmation
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ReviewSerializer, 
    ProductReviewSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    UserConfirmSerializer
)

# ==========================================
# AUTHENTICATION SYSTEM
# ==========================================

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()
            
            code = UserConfirmation.generate_code()
            UserConfirmation.objects.create(user=user, code=code)
            
            print(f"--- CONFIRMATION CODE FOR {username}: {code} ---")
            
            return Response(
                {"message": "User registered successfully! Please confirm your account.", "code_debug": code}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            code = serializer.validated_data['code']
            
            try:
                confirmation = UserConfirmation.objects.get(user__username=username, code=code)
                user = confirmation.user
                user.is_active = True
                user.save()
                confirmation.delete()
                
                return Response({"message": "Account activated successfully! You can now log in."}, status=status.HTTP_200_OK)
            except UserConfirmation.DoesNotExist:
                return Response({"error": "Invalid username or confirmation code."}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials or account not activated yet."}, status=status.HTTP_401_UNAUTHORIZED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# CATEGORY ENDPOINTS
# ==========================================

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.annotate(products_count=Count('products'))
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    def get_object(self, id):
        queryset = Category.objects.annotate(products_count=Count('products'))
        return get_object_or_404(queryset, id=id)

    def get(self, request, id):
        category = self.get_object(id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, id):
        category = self.get_object(id)
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================================
# PRODUCT ENDPOINTS
# ==========================================

class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewsListAPIView(APIView):
    def get(self, request):
        products = Product.objects.prefetch_related('reviews').annotate(
            average_rating=Avg('reviews__stars')
        )
        serializer = ProductReviewSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailAPIView(APIView):
    def get_object(self, id):
        queryset = Product.objects.prefetch_related('reviews').annotate(
            average_rating=Avg('reviews__stars')
        )
        return get_object_or_404(queryset, id=id)

    def get(self, request, id):
        product = self.get_object(id)
        serializer = ProductReviewSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        # We fetch via regular Product lookup since we're updating general product details
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================================
# REVIEW ENDPOINTS
# ==========================================

class ReviewListAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAPIView(APIView):
    def get_object(self, id):
        return get_object_or_404(Review, id=id)

    def get(self, request, id):
        review = self.get_object(id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, id):
        review = self.get_object(id)
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        review = self.get_object(id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)