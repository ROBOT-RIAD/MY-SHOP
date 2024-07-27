from django.contrib import admin
from accounts.models import User,UserAccounts
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)
class UserAccountsAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'full_name', 'address', 'city', 'zipcood', 'country', 'phone', 'date_join')
    search_fields = ('user__email', 'username', 'full_name', 'city', 'country')

admin.site.register(UserAccounts, UserAccountsAdmin)