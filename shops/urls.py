from django.urls import path,include
from shops.views import ProductDetailView
urlpatterns = [
    path("product-details/<int:id>",ProductDetailView.as_view(),name="detail")
    
]