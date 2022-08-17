from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

from carts.views import _cart_id
from carts.models import Cart,CartItem
from .models import Account
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if 'email' in request.session:
        return redirect('/homepage')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        print(email)
        print(password)
        # user = auth.authenticate(email=email, password=password)
        # if user is not None:
        #     auth.login(request,user)
        #     return HttpResponse('<h1>Logged IN</h1>')
        user = Account.objects.all()
        for i in user:
            
            print(i.email)
            print(i.password)
            if email == i.email and password == i.password:
                
                try :
                    cart=Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item =CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user_id= i.id
                            item.save()
                except :
                    pass
                print("l succes")
                if i.is_blocked == True:
                    request.session['uid'] = i.id
                    return JsonResponse(
                    {
                        'success':True},

                                safe=False
                            
                            )
                else:
                    request.session['email'] = i.email
                    request.session['uid'] = i.id
                    request.session['first_name'] = i.first_name
                    request.session['last_name'] = i.last_name
                
               
                    return JsonResponse(
                    {
                        'success':True},

                                safe=False
                            
                            )
        else:
                return JsonResponse(
                {'success':False
                },
                safe=False
            )   
    return render(request, 'login.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if 'email' in request.session:
        return redirect('/homepage')
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password1'] 
        user = Account(first_name = first_name, last_name = last_name, Phone_number = phone, email = email, password = password)
        user.save()
        return redirect(user_login)
    return render(request, 'register.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect("/")