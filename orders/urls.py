from django.urls import path,include
from .views import AddToCartView,CartView,RemoveCartView,IncreaseCartView,DecreaseCartView

urlpatterns = [
    path('add-to-cart/<int:id>/', AddToCartView.as_view(), name='addtocart'),
    path('cart/',CartView.as_view(),name='cart'),
    path('remove_cart/<int:id>/', RemoveCartView.as_view(), name='removecart'),
    path('increase-cart/<int:id>/', IncreaseCartView.as_view(), name='increasecart'),
    path('decrease-cart/<int:id>/', DecreaseCartView.as_view(), name='decreasecart'),
]