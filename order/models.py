from django.db import models
from customer.models import Customer
from sim_manager.models import SIM

class Order(models.Model):
    # Thông tin đơn hàng
    full_name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Họ và tên')
    phone_number = models.CharField(max_length=20, blank=False, null=False, verbose_name='Số điện thoại')
    email = models.EmailField(blank=False, null=False, verbose_name='Email')
    address = models.CharField(max_length=250, blank=False, null=False, verbose_name='Địa chỉ')
    gender = models.CharField(max_length=1, choices=(('M', 'Nam'), ('F', 'Nữ')), blank=True, null=True, verbose_name='Giới tính')
    order_date = models.DateTimeField(auto_now_add=True, editable=False, blank=False, null=False, verbose_name='Thời gian đặt')
    message = models.CharField(max_length=500, blank=True, null=True, verbose_name="Yêu cầu khách hàng")
    
    #Tài khoản đặt
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Khách hàng", related_name="orders")

    #Thông tin đăng ký sim
    cccd_image = models.ImageField(upload_to='cccd_images/', blank=True, null=True, verbose_name='Ảnh CCCD đăng ký')
    portrait_image = models.ImageField(upload_to='portrait_images/', blank=True, null=True, verbose_name= 'Ảnh chân dung đăng ký')
    
    # Thông tin thanh toán
    PAYMENT_METHODS = (
        ('COD', 'Trả tiền khi nhận hàng'),
        ('TRANSFER', 'Chuyển khoản'),
    )
    
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=10, verbose_name="Phương thức thanh toán")
    is_paid = models.BooleanField(default=False, verbose_name='Trạng thái thanh toán')
    paid_date = models.DateTimeField(blank=True, null=True, verbose_name='Ngày thanh toán')

    # Trạng thái đơn hàng
    ORDER_STATUSES = (
        ('PENDING', 'Chuẩn bị tiếp nhận'),
        ('PROCESSING', 'Đang xử lý'),
        ('SHIPPING', 'Đang giao hàng'),
        ('DELIVERED', 'Đã giao hàng'),
        ('REFUNDED', 'Đã hoàn'),
        ('CANCELLED', 'Đã hủy'),
    )
    order_status = models.CharField(choices=ORDER_STATUSES, max_length=20, verbose_name='Trạng thái đơn')

    # Thông tin vận chuyển
    tracking_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='Mã đơn vận')
    shipping_provider = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nhà vận chuyển')
    ship_date = models.DateTimeField(blank=True, null=True, verbose_name='Ngày giao hàng')

    def __str__(self):
        return f"{self.full_name}'s Order"


    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural  = "Danh sách đơn hàng"
        
    def get_customer_username(self):
        return self.customer.username
    get_customer_username.short_description = "Người đặt"
        
    def get_gender_display(self):
        if self.gender == 'M':
            return 'Nam'
        return 'Nữ'
    get_gender_display.short_description = "Giới tính"
    
    def get_order_status_display(self):
        return dict(Order.ORDER_STATUSES).get(self.order_status, '')
    get_order_status_display.short_description = "Trạng thái đơn hàng"
    
    def get_payment_method_display(self):
        return dict(Order.PAYMENT_METHODS).get(self.payment_method, '')
    get_payment_method_display.short_description = "Phương thức thanh toán"
    
    def get_paid_state_display(self):
        if self.is_paid: 
            return "Đã thanh toán"
        return "Chưa thanh toán"
    get_payment_method_display.short_description = "Trạng thái thanh toán"
    
    def get_total_price(self):
        total_price = 0
        for item in OrderItem.objects.filter(order = self):
            total_price += item.sim.get_curr_price()
        return "{:,.0f}".format(total_price) + " đ"
    get_total_price.short_description = 'Tổng giá'

class OrderItem(models.Model):
    sim = models.ForeignKey(SIM, on_delete=models.CASCADE, verbose_name="Sim", related_name="order_item")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Sim", related_name="order_items")
    
    def __str__(self):
        return self.sim.phone_number
    
    class Meta:
        verbose_name = 'Sim'
        verbose_name_plural  = "Danh sách SIM"
        unique_together = ['sim', 'order']
        
    def get_phone_number(self):
        return self.sim.phone_number
    get_phone_number.short_description = "Số điện thoại"

    def get_network_name(self):
        return self.sim.network.name
    get_network_name.short_description = "Nhà mạng"

    def get_original_price_str(self):
        return self.sim.get_originalpricestr()
    get_original_price_str.short_description = "Giá gốc"

    def get_sale_price_str(self):
        return self.sim.get_salepricestr()
    get_sale_price_str.short_description = "Giá sau giảm"

    def get_discount(self):
        return self.sim.get_discount()
    get_discount.short_description = "Giảm"
    
    def get_total_price(self):
        total_price = 0
        for item in OrderItem.objects.filter(id = self.order.id):
            total_price += item.sim.get_curr_price()
        return "{:,.0f}".format(total_price) + " đ"
    get_total_price.short_description = 'Tổng giá'
