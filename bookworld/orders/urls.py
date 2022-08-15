from django.urls import URLPattern, path
from . import views
urlpatterns = [
    # path('',views.product_view,name="productview"),
    
    path('palce_order/',views.place_order,name='place_order'),
    path('review_checkout/',views.review_checkout,name='review_checkout'),
    path('payment/<int:order_number>/<int:order_id>/<int:total>',views.payment,name='payment'),
    # path('place_order/<str:pay>',views.payment,name='payments'),
    path('order_history',views.order_history,name="order_history"),
    path('cancel_order/<int:oid>',views.cancel_order,name='cancel_order')
]