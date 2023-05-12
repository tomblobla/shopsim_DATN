from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['get_phone_number', 'get_network_name', 'get_original_price_str', 'get_sale_price_str', 'get_discount', 'get_total_price']
    extra = 0
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    
    list_display = ['full_name', 'phone_number', 'email', 'address', 'customer', 'order_date', 'order_status', 'get_customer_username']
    search_fields = ['full_name', 'phone_number', 'email']
    list_filter = ['order_status', 'is_paid', 'payment_method']
    
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('full_name', 'phone_number', 'email', 'address', 'gender', 'message', 'customer')
        }),
        ('Thông tin đăng ký sim', {
            'fields': ('cccd_image', 'portrait_image')
        }),
        ('Thanh toán', {
            'fields': ('payment_method', 'is_paid', 'paid_date')
        }),
        ('Trạng thái đơn hàng', {
            'fields': ('order_status',)
        }),
        ('Thông tin vận chuyển', {
            'fields': ('tracking_number', 'shipping_provider', 'ship_date')
        }),
    )

admin.site.register(Order, OrderAdmin)
