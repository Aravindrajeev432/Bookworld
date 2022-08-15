from unicodedata import name
from django.urls import URLPattern, path
from . import views
urlpatterns = [
    path('login',views.adminlogin,name="adminlogin"),
    path('logout',views.logout,name='adminlogout'),
    path('dashboard',views.dashboard,name="dashboard"),
    path('products',views.products,name='products'),
    path('addnewbook',views.addnewbook,name="addnewbook"),
    path('category_management',views.category_management,name="addnewcategory"),
    path('delete_cat/<int:id>',views.delete_cat,name='delete_cat'),
    path('edit_book/<int:id>',views.edit_book,name="editbook"),
    path('unblock_book/<int:id>',views.unblock_book,name='unblock_book'),
    path('block_book/<int:id>',views.block_book,name="block_book"),
    path('delete_book/<int:id>',views.delete_book,name="deletebook"),
    path('users',views.users,name="usersview"),
    path('edit_user/<int:id>',views.edit_user,name='block_unblock'),
    path('block_user/<int:id>',views.block_user,name='block_user'),
    path('unblock_user/<int:id>',views.unblock_user,name='unblock_user'),
    path('delete_user/<int:id>',views.delete_user,name='delete_user'),
    path('order_management',views.order_management,name='order_management'),
    path('change_order_status/<str:st>/<int:oid>/<int:pid>',views.change_order_status,name="order_status_change"),
   
            ]