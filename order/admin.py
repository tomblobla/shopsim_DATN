from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import mark_safe

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['get_phone_number', 'get_network_name', 'get_original_price_str', 'get_sale_price_str', 'get_discount', 'get_total_price']
    extra = 0
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    
    list_display = ['full_name', 'phone_number', 'email', 'address', 'customer', 'order_date', 'order_status', 'get_customer_username', 'is_paid', 'goto_invoice']
    search_fields = ['full_name', 'phone_number', 'email']
    list_filter = ['order_status', 'is_paid', 'payment_method']
    readonly_fields = ('goto_invoice', )
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('full_name', 'phone_number', 'email', 'address', 'gender', 'message', 'customer', 'goto_invoice')
        }),
        ('Thông tin đăng ký sim', {
            'fields': ('cccd_image', 'portrait_image')
        }),
        ('Thanh toán', {
            'fields': ('payment_method', 'is_paid', 'paid_date', 'transaction_id')
        }),
        ('Trạng thái đơn hàng', {
            'fields': ('order_status',)
        }),
        ('Thông tin vận chuyển', {
            'fields': ('tracking_number', 'shipping_provider', 'ship_date')
        }),
    )
    
    
    
    
    def goto_invoice(self, obj):  # new
        
        return mark_safe(f"""<a href="/don-hang/xem-hoa-don/{obj.id}" style="display: inline-block; padding: 7px 15px; border: none; border-radius: 5px; color: #fff; background-color: #47bac1; text-decoration: none; transition: all 0.3s ease;"
                         onmouseover="this.style.backgroundColor='#639af5'"
                            onmouseout="this.style.backgroundColor='#47bac1'"
  >
                Xem hóa đơn
                </a>""")
    goto_invoice.short_description = ""
    goto_invoice.allow_tags = True  # Needed for HTML rendering in Django 3.x and above


admin.site.register(Order, OrderAdmin)
