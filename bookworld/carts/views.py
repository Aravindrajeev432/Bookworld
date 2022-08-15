from itertools import product
from re import T
from django.shortcuts import get_object_or_404, redirect, render
from . models import Cart, CartItem
from store.models import Product
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control
# Create your views here.

def cart(request,total = 0 ,quantity= 0, cart_items = None):
    if 'first_name' in request.session:
        try :
            uid=request.session['uid']
   
            cart_items = CartItem.objects.filter(user_id=uid, is_active=True)
            for cart_item in cart_items:
                total +=(cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
        except ObjectDoesNotExist:
            pass
        context = {
            'total' : total,
            'quantity' :quantity,
            'cart_items' : cart_items,
        }
        return render(request,'store/cart.html',context)
        
    else:
        try:
            
            cart =Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total +=(cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
        except ObjectDoesNotExist:
            pass
        context = {
            'total' : total,
            'quantity' :quantity,
            'cart_items' : cart_items,
        }
        return render(request,'store/cart.html',context)

def _cart_id(request):
    cart =request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    print(type(product))
    print("dkfsdfsdf")
    try :
        if 'uid' in request.session:
            pass
        else:
            cart =Cart.objects.get(cart_id= _cart_id(request) )
    except Cart.DoesNotExist:
        if 'uid' in request.session:
            pass
        else:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()    
    try :
        if 'uid' in request.session:
            uid= request.session['uid']
            cart_item = CartItem.objects.get(product=product, user_id=uid) 
        else:
            
            cart_item = CartItem.objects.get(product=product, cart=cart) 
        cart_item.quantity += 1
        cart_item.save()
        
    except CartItem.DoesNotExist:
        if 'uid' in request.session:
            uid= request.session['uid']
            cart_item = CartItem.objects.create(
                product =product,
                quantity = 1,
                user_id = uid
            )
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )  
            cart_item.save()
    return redirect('cart')

def remove_cart(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    if 'uid' in request.session:
         uid=request.session['uid']
         cart_item = CartItem.objects.get(product=product,user_id=uid)
    else :
        
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def delete_cart(request,product_id):
    if 'uid' in request.session:
        uid= request.session['uid']
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product,user_id=uid)
    else:
        
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def checkout(request,total = 0 ,quantity= 0, cart_items = None):
    try :
        if 'uid' in request.session:
            uid = request.session['uid']
            cart_items = CartItem.objects.filter(user_id=uid, is_active=True)
        else:
            cart =Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    context = {
        'total' : total,
        'quantity' :quantity,
        'cart_items' : cart_items,
    }
    return render(request,'store/checkout.html',context)

