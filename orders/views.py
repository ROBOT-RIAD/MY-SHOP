from django.shortcuts import get_object_or_404, redirect,render
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from orders.models import Order, Cart
from shops.models import Product

class AddToCartView(View):
    def get(self, request, id):
        return self.add_to_cart(request, id)
    
    def post(self, request, id):
        return self.add_to_cart(request, id)

    def add_to_cart(self, request, id):
        if not request.user.is_authenticated:
            messages.info(request, "You need to be logged in to add items to the cart.")
            return redirect('login')
        
        item = get_object_or_404(Product, pk=id)
        order_item, created = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_query = Order.objects.filter(user=request.user, ordered=False)
        
        if order_query.exists():
            order = order_query[0]
            if order.orderitems.filter(item=item).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item's quantity was updated.")
            else:
                order.orderitems.add(order_item)
                messages.info(request, "This item was added to your cart.")
        else:
            order = Order(user=request.user)
            order.save()
            order.orderitems.add(order_item)
            messages.info(request, "This item was added to your cart.")
        
        return redirect('home')
    

class CartView(View):
    def get(self, request, *args, **kwargs):
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            return render(request, 'cart.html', {'carts': carts, 'order': order})
        else:
            messages.warning(request, "You do not have any items in your cart")
            return redirect('home')
        


class RemoveCartView(View):
    def get(self, request, id):
        return self.handle_remove(request, id)
    
    def post(self, request, id):
        return self.handle_remove(request, id)

    def handle_remove(self, request, id):
        item = get_object_or_404(Product, pk=id)
        order_query = Order.objects.filter(user=request.user, ordered=False)
        
        if order_query.exists():
            order = order_query[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
                order_item = order_item[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.info(request, "This item was removed from your cart")
                return redirect('home')
            else:
                messages.info(request, "This item was not in your cart")
                return redirect('home')
        else:
            messages.info(request, "You don't have an active order")
            return redirect('home')
        

class IncreaseCartView(View):
    def get(self, request, id, *args, **kwargs):
        return self.handle_increase(request, id, *args, **kwargs)
    
    def post(self, request, id, *args, **kwargs):
        return self.handle_increase(request, id, *args, **kwargs)

    def handle_increase(self, request, id, *args, **kwargs):
        item = get_object_or_404(Product, pk=id)
        order_query = Order.objects.filter(user=request.user, ordered=False)
        
        if order_query.exists():
            order = order_query[0]
            order_item, created = Cart.objects.get_or_create(
                order=order,
                item=item,
                user=request.user,
                purchased=False
            )
        
            if not created:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"Quantity of {item.name} increased.")
            else:
                messages.info(request, f"{item.name} added to your cart.")
            
            return redirect('cart')
        else:
            messages.info(request, "You do not have an active order.")
            return redirect('home')
        



class DecreaseCartView(View):
    def get(self, request, id, *args, **kwargs):
        return self.handle_decrease(request, id, *args, **kwargs)
    
    def post(self, request, id, *args, **kwargs):
        return self.handle_decrease(request, id, *args, **kwargs)

    def handle_decrease(self, request, id, *args, **kwargs):
        item = get_object_or_404(Product, pk=id)
        order_query = Order.objects.filter(user=request.user, ordered=False)
        
        if order_query.exists():
            order = order_query[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.get(item=item, user=request.user, purchased=False)
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, f"Quantity of {item.name} decreased.")
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.info(request, f"{item.name} removed from your cart.")
                
                return redirect('cart')
            else:
                messages.info(request, f"{item.name} is not in your cart")
        else:
            messages.info(request, "You do not have active orders")
        
        return redirect('home')





    
