

from xml.etree.ElementInclude import include
from django.urls import URLPattern, path,include
from . import views
urlpatterns = [
    path('login',views.user_login,name="login"),
    path('register',views.register,name="register"),
    path('logout',views.logout,name="logout"),
    # path('user',include('bookworld.urls')),
    
]