from django.db import models
from accounts.models import User
from shops.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart")
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity}  {self.item}'
    
    def get_total(self):
        total = self.item.price * self.quantity
        return total
    

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264,blank=True,null=True)
    orderId =models.CharField(max_length=200,blank=True,null=True)

    def get_total(self):
        total =0
        for order_item in self.orderitems.all():
            total+= order_item.get_total()
        return total



    







