from binascii import rledecode_hqx
from itertools import product
from django.shortcuts import render,redirect
from django.http import HttpResponse
from account.models import Account
from store.models import Product
from category.models import Category
from django.views.decorators.cache import cache_control
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    try :
        uid = request.session['uid']
        is_user_blocked=Account.objects.get(id=uid)
        if is_user_blocked.is_blocked == True:
            return render(request,'userblocked.html')
    except : pass
    
    cat = Category.objects.all()
    pro = Product.objects.filter(is_active=True).all()
    paginator = Paginator(pro,6)
    page = request.GET.get('page')
    paged_products =paginator.get_page(page)
    
    
    
    return render(request, 'landing.html',{'category':cat,'pro':paged_products})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    pro = Product.objects.all()
    
    
    return render(request, 'landing.html',{'pro':pro})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homepage(request):
    if 'email' in request.session:
        return render(request,'home.html')
    else:
        return redirect('/')

