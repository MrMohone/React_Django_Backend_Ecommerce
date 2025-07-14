from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, DetailedProductSerializer,CartItemSerializer,SimpleCartSerializer,CartSerializer
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
        cart_code = request.data.get("cart_code")#get from front end localStorage
        product_id = request.data.get('product_id')
        #If exist a cart, get a cart else create new cart
        #1st 'cart' is object created(Cart), 2nd 'created' is boolean (created) whether True or Fals
        cart, created = Cart.objects.get_or_create(cart_code=cart_code)#created cart
        product = Product.objects.get(id=product_id)
        
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity = 1
        cartitem.save()
        
        serializer = CartItemSerializer(cartitem)
        return Response({'data':serializer.data, 'message': 'CartItem created Successfully'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['GET'])
def product_in_cart(request):
    cart_code = request.query_params.get('cart_code')# get cart_code from front end localStorage
    product_id = request.query_params.get('product_id')

    cart = Cart.objects.get(cart_code=cart_code)
    product = Product.objects.get(id=product_id)

    products_exists_in_cart = CartItem.objects.filter(cart=cart, product=product).exists()
    
    return Response({'product_in_cart' : products_exists_in_cart})


@api_view(['GET'])
def get_cart_stat(request):
    cart_code = request.query_params.get('cart_code')# get cart_code from front end localStorage
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    
    serializer = SimpleCartSerializer(cart)
    return Response(serializer.data)

@api_view(['GET'])
def get_cart(request):
    cart_code = request.query_params.get('cart_code')# get cart_code from front end localStorage
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['PATCH'])# used to update specific field
def update_quantity(request):
    try:
        cartitem_id = request.data.get('item_id')# get cartitem_id from front end
        quantity = request.data.get('quantity')# get quantity from front end
        quantity = int(quantity)# convert to integer
        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({'data': serializer.data, 'message': 'CartItem updated Successfully'}, status=200)
    
    except Exception as e:
        return Response({'error': str(e)}, status=400)