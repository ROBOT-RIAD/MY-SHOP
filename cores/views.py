from django.shortcuts import render
from shops.models import Product
from django.views.generic import ListView,DateDetailView
# Create your views here.

class HomeView(ListView):
    model = Product
    template_name = 'cores/index.html'
    context_object_name = 'products'
