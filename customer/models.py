from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.html import mark_safe
from sim_manager.models import SIM

# Tạo manager để quản lý tài khoản khách hàng
class CustomerAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, gender, address, phone_number, password=None):
        if not email:
            raise ValueError("Khách hàng phải có email.")
        if not username:
            raise ValueError("Khách hàng phải có tên đăng nhập.")
        if not first_name:
            raise ValueError("Khách hàng phải điền tên.")
        if not last_name:
            raise ValueError("Khách hàng phải điền họ.")
        if not gender:
            raise ValueError("Khách hàng phải điền giới tính.")
        if not address:
            raise ValueError("Khách hàng phải điền địa chỉ.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            gender = gender,
            address = address,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password, first_name, last_name, gender, address, phone_number):
        if not email:
            raise ValueError("Khách hàng phải có email.")
        if not username:
            raise ValueError("Khách hàng phải có tên đăng nhập.")
        if not first_name:
            raise ValueError("Khách hàng phải điền tên.")
        if not last_name:
            raise ValueError("Khách hàng phải điền họ.")
        if not gender:
            raise ValueError("Khách hàng phải điền giới tính.")
        if not address:
            raise ValueError("Khách hàng phải điền địa chỉ.")

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            gender = gender,
            address = address,
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# Model Khách hàng
class Customer(AbstractBaseUser):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Nam'),
        (FEMALE, 'Nữ'),
    )

    first_name = models.CharField(max_length=30, blank=True, verbose_name='Tên')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Họ')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, verbose_name='Giới tính')
    address = models.CharField(max_length=200, blank=True, verbose_name='Địa chỉ')
    email = models.EmailField(unique=True, verbose_name='Địa chỉ email', blank=True)
    phone_number = models.CharField(max_length=30, verbose_name='Số điện thoại', unique=True, blank=True)
    username = models.CharField(max_length=30, unique=True, verbose_name='Tên đăng nhập')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    is_admin = models.BooleanField(default=False, verbose_name='Là Admin')

    objects = CustomerAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'gender', 'address']

    class Meta:
        verbose_name = 'Khách hàng'
        verbose_name_plural  = "Danh sách Khách hàng"
        
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def resend_activate_email(self):  # new
        return mark_safe(f"""<a href="/tai-khoan/gui-lai-email-xac-nhan/{self.username}" style="display: inline-block; padding: 7px 15px; border: none; border-radius: 5px; color: #fff; background-color: #47bac1; text-decoration: none; transition: all 0.3s ease;"
                         onmouseover="this.style.backgroundColor='#639af5'"
                            onmouseout="this.style.backgroundColor='#47bac1'"
  >
                Gửi lại mail kích hoạt
                </a>""")
    resend_activate_email.short_description = ""

class CartItem(models.Model):
    sim = models.ForeignKey(SIM, on_delete=models.CASCADE, verbose_name="Sim", related_name="cart_items")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Khách hàng", related_name="cart_items")
    added_date = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return self.sim.phone_number
    
    class Meta:
        verbose_name = 'Sim'
        verbose_name_plural  = "Giỏ hàng"
        unique_together = ['sim', 'customer']
        
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
        for item in CartItem.objects.filter(customer=self.customer):
            total_price += item.sim.get_curr_price()
        return "{:,.0f}".format(total_price) + " đ"

    get_total_price.short_description = 'Tổng giá'
