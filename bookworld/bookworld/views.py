from binascii import rledecode_hqx
import email
from itertools import product
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from account.models import Account,Address
from orders.models import OrderProduct,Order
from store.models import Product
from category.models import Category
from django.views.decorators.cache import cache_control
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ProfileForm
from collections import Counter
from django.db.models import Sum,Count
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request,id):
  
    user_details = Account.objects.get(id=id)
    print(id)
    try:
        user_address = Address.objects.get(user_id=id)
        print(user_address)
        print(user_address.address_line_2)
    except:
        user_address = " "
    try:
        f_cat=[]
        fav_cat= OrderProduct.objects.filter(user=id).values('product_id')
      
        for fav in fav_cat:
            
            p_id=fav['product_id']
            cat= Product.objects.filter(id=p_id).values('category_id')
            for c in cat:
                
    
                f_cat.append(c['category_id'])
       
        c = Counter(f_cat)
        ca = c.most_common(1)
       
        fav_category_id = ca[0][0]
        fav_category = Category.objects.get(id=fav_category_id)
       
        fav_category_name = fav_category.category_name
    except  :
        print("except")
        
        fav_category_name = "Please Buy Atlest One Book"
    
    try :
        books_buyed = OrderProduct.objects.filter(user=id).values('user').annotate(count=Count('quantity'))
        books_buyed=list(books_buyed)
        books_buyed=books_buyed[0]
        books_buyed=books_buyed["count"]
    except:
        print("book_buyed exception")
        books_buyed=0
        
    
    context={
        'user':user_details,
        'fav_category' : fav_category_name,
        'books_buyed': books_buyed,
        'user_address':user_address,
    }

    
    return render(request,'user_profile.html',context)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_address(request,id):
    uid = request.session['uid']
    
    if request.method == 'POST':
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        zipcode = request.POST['zipcode']
        print(address_line_1)
        print(address_line_2)
        print(country)
        print(state)
        print(city)
        print(zipcode)
       
        try :
            user_address = Address.objects.get(user_id=uid)
            user_address.address_line_1 = address_line_1
            user_address.address_line_2 = address_line_2
            user_address.country = country
            user_address.state = state
            user_address.city = city
            user_address.zipcode = zipcode
            user_address.save() 
        except:
            user = Address(address_line_1 = address_line_1, address_line_2 = address_line_2,user_id = uid, country = country, state = state, city = city,zipcode = zipcode)
            user.save()
        
        
        return JsonResponse(
                    {
                        'success':True},

                                safe=False
                            
                            )
    return JsonResponse(
                    {
                        'success':False},

                                safe=False
                            
                            )

def editprofile(request,id):
    user_edit = Account.objects.get(id=id)
    
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
       
        user_edit.first_name = fname
        user_edit.last_name = lname
        user_edit.email = email
        user_edit.Phone_number = phone
        user_edit.save()
    
        return JsonResponse(
                    {
                        'success':True},

                                safe=False
                            
                            )
    
    return JsonResponse(
                    {
                        'success':False},

                                safe=False
                            
                            )