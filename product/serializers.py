from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):

    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = 'id name products_count'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title description price category'.split()


class ProductReviewSerializer(serializers.ModelSerializer):
    # Nested reviews - this uses the 'related_name' from your ForeignKey
    reviews = ReviewSerializer(many=True, read_only=True)
    
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = 'id title reviews average_rating'.split()