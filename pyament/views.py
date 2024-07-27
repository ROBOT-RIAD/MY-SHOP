from django.shortcuts import render ,redirect,HttpResponseRedirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from pyament.models import BillingAddress
from pyament.forms import BillingForm
from orders.models import Order,Cart
from sslcommerz_lib import SSLCOMMERZ 
import random,string
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
from django.contrib import messages

def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class CheckoutView(FormView):
    template_name = 'checkout.html'
    form_class = BillingForm
    success_url = reverse_lazy('checkout')  # Redirects to the same view on success

    def get_form(self, form_class=None):
        user = self.request.user
        saved_address, _ = BillingAddress.objects.get_or_create(user=user)
        return self.form_class(instance=saved_address, **self.get_form_kwargs())

    def form_valid(self, form):
        saved_address = form.save(commit=False)
        saved_address.user = self.request.user
        saved_address.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        order_query = Order.objects.filter(user=user, ordered=False)
        
        if order_query.exists():
            order = order_query.first()
            context['order_items'] = order.orderitems.all()
            context['order_total'] = order.get_total()
        else:
            context['order_items'] = []
            context['order_total'] = 0
        
        # Get the saved billing address and check if all fields are filled
        saved_address, _ = BillingAddress.objects.get_or_create(user=user)
        context['is_address_complete'] = saved_address.is_full_fields()
        
        return context
    

def Pyament(request):  
    order_query = Order.objects.filter(user=request.user,ordered =False)[0]
    order_items =order_query.orderitems.all()
    order_total =order_query.get_total()


    settings = { 'store_id': 'mysho668eb5535fb5c', 'store_pass': 'mysho668eb5535fb5c@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = order_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = unique_transaction_id_generator()
    post_body['success_url'] =f"http://127.0.0.1:8000/pyament/purchase/{post_body['tran_id']}/{request.user.id}/"
    post_body['fail_url'] = "http://127.0.0.1:8000/orders/cart/"
    post_body['cancel_url'] = "http://127.0.0.1:8000/orders/cart/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = request.user.email
    post_body['cus_email'] = request.user.email
    post_body['cus_phone'] = "01700000000"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    print(response)
    # Need to redirect user to response['GatewayPageURL']
    return redirect(response['GatewayPageURL'])

@csrf_exempt
def purchase(request,tran_id,user_id):
    user =User.objects.get(id=user_id)
    order_query = Order.objects.filter(user=user,ordered =False)
    order=order_query[0]
    order.ordered = True
    order.orderId =tran_id
    order.paymentId =tran_id

    cart_items = Cart.objects.filter(user=user,purchased =False)

    for item in cart_items:
        item.purchased =True
        item.save()

    return HttpResponseRedirect(reversed('vieworder'))


@csrf_exempt
def ViewOrder(request):
    orders =Order.objects.filter(user=request.user,ordered = True)
    if orders:
        context ={"orders": orders}    
    else:
        messages.warning(request,"you dont have any orders")
        return redirect("home")
    return render(request,'order.html',context)

    






    
