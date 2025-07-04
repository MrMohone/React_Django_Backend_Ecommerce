from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','slug','image','descriptions','category','price']
        
class DetailedProductSerializer(serializers.ModelSerializer):
    similar_products = serializers.SerializerMethodField()
    fields = ['id', 'name', 'price', 'slug', 'image', 'description', 'similar_products']
    
    def get_similar_products(self, product):
        products = Product.objects.filter(category=Product.category).exclude(id=product.id)
        serializer = ProductSerializer(products, many=True)
        return serializer.data