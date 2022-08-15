from cgi import print_directory
import imp
from unicodedata import category
from django.forms import PasswordInput
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from account.models import Account
from orders.models import Order,OrderProduct
from store.models import Product
from category.models import Category
from store.forms import ProductForm
# from category.forms import category_form
from django.contrib import auth,messages
# from slugify import slugify
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum,Count
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        user = Account.objects.all()
        for i in user:
            
            print(i.email)
            print(i.password)
            print(i.is_admin)
            if email == i.email and password == i.password and i.is_admin == True:
                print("l succes")
                request.session['admin'] = True
                
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
        

    return render(request,'admin/adminlogin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect("/")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    usercount= Account.objects.filter(~Q(is_admin=True)).count()
    p_count = Product.objects.count()
    # order_graph=Order.objects.aggregate(Sum('order_total'))
    # order_graph = OrderProduct.objects.all()
    order_graph =Order.objects.filter().values('created_at__date').order_by('created_at__date')[:7].annotate(sum=Sum('order_total'))
    order_status_graph =OrderProduct.objects.filter().values('status').annotate(count=Count('status'))
    order_product_count_graph = OrderProduct.objects.filter().values('quantity').order_by('created_at__date')[:7].annotate(count=Count('quantity'))
                                                                                                                          
    print("--------")
    print(order_product_count_graph)
    print("-------")
    # print(order_graph)
    # for i in order_graph:
    #     print(i['sum'])    
    return render(request, 'admin/dashboard.html',{'usercount':usercount,'p_count':p_count,'order_total_graph':order_graph,'order_status_graph':order_status_graph})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def products(request):
    if 'admin' not in request.session:
        return redirect('login')
    book_selled_count = OrderProduct.objects.filter(status='Deliverd').count()
    new_orders = OrderProduct.objects.filter(status='Processing').count()
    p_count = Product.objects.count()
    outofstock = Product.objects.filter(book_count=0).count()
    product = Product.objects.all().order_by('book_name')
    if request.method == 'POST':
        s = request.POST['search']
        product = Product.objects.filter(book_name__icontains=s)
    
    p = Paginator(product,6)
    page = request.GET.get('page',1)
    pro = p.get_page(page)
    
    cat = Category.objects.all()
    return render(request,'admin/productmanagement.html',{'product':product,'cat':cat,'p_count':p_count,'outofstock':outofstock,'pro':pro,'book_selled_count':book_selled_count,'new_orders':new_orders})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_book(request, id):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    if request.method == 'POST':
        bookedit = Product.objects.get(id=id)
        bookedit.book_name = request.POST.get('book_name')
        bookedit.author = request.POST.get('author_name')
        bookedit.description = request.POST.get('description')
        bookedit.price = request.POST.get('price')
        
        
        bookedit.category_id = request.POST.get('category')
        bookedit.book_count = request.POST.get('stock')
        if len(request.FILES) != 0:
            bookedit.image = request.FILES.get('image')
        bookedit.save()
        messages.success(request, 'Profile details updated.')
    book_details = Product.objects.get(id=id)
    category = Category.objects.all()
    return render(request,'admin/edit_book.html',{'book_details':book_details,'category':category})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def unblock_book(request, id):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    bookun = Product.objects.get(id=id)
 
    bookun.is_active=True
    bookun.save()
    return redirect(products)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_book(request, id):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    bookbl = Product.objects.get(id=id)
    re= request.GET.get('page')
    print(re)
    bookbl.is_active=False
    bookbl.save()
    return redirect(products)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_book(request, id):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    bookdel= Product.objects.get(id=id)
    bookdel.delete()
    return redirect(products)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addnewbook(request):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    form = ProductForm()
    # if request.method == 'POST':
    #     print(f)
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            # print(form.cleaned_data['book_name'])
            
            # sl= slugify(form.cleaned_data['book_name']) 
            # print(sl)
            form.save() 
            form = ProductForm() 
            messages.error(request,'Successfuly Added')
    cat = Category.objects.only('category_name')
    return render(request,'admin/addnewbook.html',{'cat':cat,'form':form})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletebook(request):
    pass
def editbook(request):
    pass
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category_management(request):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    category = Category.objects.all()
    if request.method == 'POST':
        
        category_name = request.POST['category_name']
        if not Category.objects.filter(category_name=category_name).exists():
        
            cat = Category(category_name=category_name)
            cat.save()
        else:
            messages.error(request,'This category already exists')
    
    return render(request,'admin/addnewcategory.html',{'category':category})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_cat(request,id):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    pass
    del_cat = Category.objects.get(id=id)
    del_cat.delete()
    return redirect(category_management)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def users(request):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    account = Account.objects.filter(~Q(is_admin=True))

    usercount= Account.objects.filter(~Q(is_admin=True)).count()

    blocked_users_count = Account.objects.filter(is_blocked=True).count()
    active_users_count = usercount - blocked_users_count
    paginator = Paginator(account,6)
    page = request.GET.get('page')
    accounts =paginator.get_page(page)
    if request.method == 'POST':
        s = request.POST['search']
        account = Account.objects.filter(first_name__startswith=s)
        
        return render(request,'admin/usersview.html',{'account':accounts,'usercount':usercount,'blocked_users_count':blocked_users_count,'active_users_count':active_users_count})
    
    return render(request,'admin/usersview.html',{'account':accounts,'usercount':usercount,'blocked_users_count':blocked_users_count,'active_users_count':active_users_count})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_user(request, id):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    if request.method == 'POST':
        useredit = Account.objects.get(id=id)
        useredit.first_name = request.POST.get('first_name')
        useredit.last_name = request.POST.get('last_name')
        useredit.email = request.POST.get('email')
        useredit.Phone_number = request.POST.get('phone')

        useredit.save()
        messages.success(request, 'Profile details updated.')
        

    user = Account.objects.get(id=id)   
    return render(request,'admin/edituser.html',{'user':user})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_user(request, id):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    b_user = Account.objects.get(id=id)
    print(b_user.is_blocked)
    b_user.is_blocked=True
    b_user.save()
    print(b_user.is_blocked)
    return redirect(users)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def unblock_user(request, id):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    ub_user = Account.objects.get(id=id)
    ub_user.is_blocked=False
    ub_user.save()
    return redirect(users)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_user(request, id):
    if 'admin' not in request.session:
        return redirect('adminlogin')
    del_user = Account.objects.get(id=id)
    del_user.delete()
    return redirect(users)
# def sortbyfname(request):
    
#     return redirect(users)
def order_management(request):
    order_details = OrderProduct.objects.all().order_by('-created_at')
    p = Paginator(order_details,5)
    page = request.GET.get('page',1)
    order_details_paginated = p.get_page(page)
    total_orders_count= OrderProduct.objects.all().count()
    
    orders_pending = OrderProduct.objects.filter(status__contains='Processing').count()
    orders_deliverd = OrderProduct.objects.filter(status__contains='Deliverd').count()
    # print(orders_pending)
    context={
        'order_details':order_details_paginated,
        'total_orders_count': total_orders_count,
        'orders_pending' : orders_pending,
        'orders_deliverd' : orders_deliverd,
    }
    return render(request,'admin/ordermanagement.html',context)
    
def change_order_status(request,st,oid,pid):
    print(st)
    print(oid)
    print(pid)
    order_product_details = OrderProduct.objects.filter(product_id=pid).get(order_id=oid)
    # order_details = Order.objects.get(order_product_details.)
    order_product_details.status = st
    order_product_details.save()
    order_product_details=Order.objects.all().order_by('-created_at')
    orders_pending = OrderProduct.objects.filter(status__contains='Processing').count()
    # context={
    #     'order_details':order_details
    # }
    return HttpResponse(orders_pending)
    
    
    
    