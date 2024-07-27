from django.db import models

# to create a custom user model and admin
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy

# auto create onetoone object
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class MyUserManager(BaseUserManager):
    """email unique identifer"""
    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password"""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields)
    


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True,null=False)
    is_staff = models.BooleanField(gettext_lazy('staff status'),default=False,help_text= gettext_lazy('user log in this site'))
    is_active = models.BooleanField(gettext_lazy('active'),default=True,help_text= gettext_lazy('this field is false user can\'t login.'))
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return  self.email
    
    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
    

class UserAccounts(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='account')
    username = models.CharField(max_length=200,blank=True)
    full_name = models.CharField(max_length=200,blank=True)
    address = models.TextField()
    city = models.CharField(max_length= 50,blank=True)
    zipcood = models.CharField(max_length=10,blank=True)
    country =models.CharField(max_length=100,blank=True)
    phone = models.CharField(max_length=12,blank=True)
    date_join = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s accounts"
    
    def is_full_fields(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for fields_name in fields_names:
            value = getattr(self, fields_name)
            if value is None or value == '':
                return False
        return True


@receiver(post_save, sender=User)
def create_user_accounts(sender, instance, created, **kwargs):
    if created:
        UserAccounts.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_accounts(sender, instance, **kwargs):
    instance.account.save()
