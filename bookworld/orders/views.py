from ast import Return
from multiprocessing import context
import re
from django.shortcuts import render,redirect
from carts.models import Cart, CartItem
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control
from carts.views import _cart_id
from .forms import OrderForm
from .models import Order,Payment,OrderProduct
import datetime
# Create your views here.


def place_order(request,total = 0 ,quantity= 0, cart_items = None):
    
    print("In place Order")
    uid = request.session['uid']
    
    try :
        if 'uid' in request.session:
            uid = request.session['uid']
            cart_items = CartItem.objects.filter(user_id=uid, is_active=True)
            cart_count = cart_items.count()
            if cart_count<= 0:
                return redirect('home')
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
    
    shipping_charge= 0
    
    if request.method == 'POST':
        
        form = OrderForm(request.POST)
        
        if form.is_valid():
            print("form worked")
            data  = Order()
            data.user_id = uid
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.zipcode = form.cleaned_data['zipcode']
            data.order_total = total #just using total not grand total
            data.shipping_charge = shipping_charge
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user_id=uid,is_ordered=False,order_number=order_number)
            
            # is_orderd is is_ordered because of its in model by mistake
            context = {
                'order' : order,
                'cart_items':cart_items,
                'shipping_charge': shipping_charge,
                'total':total,
                'grand_total':total,
                'order_number':order_number,
            }
            
            
            return render(request,'store/review_checkout.html',context)
         
    return redirect('checkout')


def review_checkout(request):
    
    return render(request,'store/review_checkout.html')



def payment(request,order_number,order_id,total):
    
    uid = request.session['uid']
    # body = json.loads(request.body)
    print("payment")
    print(type(order_id))
    order = Order.objects.get(user_id=uid, is_ordered=False, order_number=order_number)

    # Store transaction details inside Payment model
    payment = Payment(
        user_id = uid,
        payment_id = order_id,
        payment_method = "COD",
        amount_paid = total,
        status = "succes",
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user_id=uid)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = uid
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

       


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.book_count -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user_id=uid).delete()

    # Send order recieved email to customer
   
    return render(request,'store/checkout_succes.html')



def order_history(request):
    if 'email' in request.session:
        uid=request.session['uid']
        order_history= OrderProduct.objects.filter(user_id=uid).order_by('-created_at')
        context={'order_history':order_history}
        
        
        
        
        
        return render(request,'orders.html',context)
    else:
        return render(request,'orders_access_denied.html')
    
def cancel_order(request,oid):
    print(oid)
    print("yeah s")
    order_cancel = OrderProduct.objects.get(id=oid)
    order_cancel.status = 'Cancelled'
    order_cancel.save()
    return redirect(order_history)