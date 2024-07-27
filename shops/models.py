from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'
    

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    image = models.ImageField(upload_to='shops/media/uploads/',blank=True,null=True)
    name = models.CharField(max_length=200)
    category =models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    preview_text =models.TextField(verbose_name='Preview text')
    detail_text =models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=12,decimal_places=2)
    old_price =models.DecimalField(max_digits=12,decimal_places=2)
    created_time =models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.name
    
    class Meta:
        ordering =["-created_time"]





