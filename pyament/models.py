from django.db import models
from accounts.models import User

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return f'{self.user.username}'
    
    def is_full_fields(self):
        for field in self._meta.get_fields():
            if isinstance(field, models.Field):  # Ensure it's a database field
                value = getattr(self, field.name)
                if value in (None, ''):
                    return False
        return True
    
    class Meta:        
        verbose_name_plural = "Billing Addresses"
