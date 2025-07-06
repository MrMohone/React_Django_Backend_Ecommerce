from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, DetailedProductSerializer,CartItemSerializer
from rest_framework.response import Response


@api_view(['GET'])
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = DetailedProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
def add_item(request):
    try:
        cart_code = request.data.get("cart_code")
        product_id = request.data.get('product_id')
        #If exist a cart, get a cart else create new cart
        #1st 'cart' is object created(Cart), 2nd 'created' is boolean (created) whether True or Fals
        cart, created = Cart.objects.get_or_create(cart_code=cart_code)#created cart
        product = Product.objects.get(id=product.id)
        
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        
        serializer = CartItemSerializer(cartitem)
        return Response({'data':serializer.data, 'message': 'CartItem created Successfully'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)