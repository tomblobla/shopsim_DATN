from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Tạo manager để quản lý tài khoản khách hàng
class CustomerAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, gender, address, password=None):
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
            gender = gender,
            address = address,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password, first_name, last_name, gender, address):
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
