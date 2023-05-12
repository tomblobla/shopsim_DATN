from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, CartItem
from jet.admin import CompactInline

# Register your models here.
class CartInline(admin.TabularInline):
    model = CartItem
    extra = 1
    show_change_link = False    
    verbose_name_plural = 'Giỏ hàng'
    verbose_name = 'Giỏ hàng'
    
    readonly_fields = [
        'get_phone_number',
        'get_network_name',
        'get_original_price_str',
        'get_discount',
        'get_sale_price_str',
    ]
    
    classes = ['collapse']


class AccountAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'phone_number',
        'first_name',
        'last_name',
        'last_login',
        'is_active',
        'is_admin'
    )

    list_display_links = ('email', 'first_name', 'last_name', 'phone_number', 'username')
    readonly_fields = ('last_login', 'resend_activate_email',)

    inlines = [CartInline,]
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Customer, AccountAdmin)
