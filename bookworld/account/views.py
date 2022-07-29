from django.shortcuts import render
from django.views.decorators.cache import cache_control
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        print(email)
        print(password)
    return render(request, 'login.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    return render(request, 'register.html')
