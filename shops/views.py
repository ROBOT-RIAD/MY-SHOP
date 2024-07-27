from django.shortcuts import render
from shops.models import Product
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class ProductDetailView(DetailView):
    model =Product
    template_name ='product_detail.html'
    pk_url_kwarg = 'id'




