from django.urls import path
from .views import CheckoutView,Pyament,purchase,ViewOrder

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('pay/',Pyament, name='payment'),
    path('orders/',ViewOrder, name='vieworder'),
    path('pyament/purchase/<str:tran_id>/<int:user_id>/', purchase, name='purchase'),
]
