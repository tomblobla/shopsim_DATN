from django.db import models
from django.utils.html import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Loại SIM')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(null=True, verbose_name='Mô tả', blank=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Ngày khởi tạo')
    
    class Meta:
        verbose_name = 'Nhãn'
        verbose_name_plural  = "Danh sách nhãn"
        
    def sim_count(self):
        return self.sims.count()
    sim_count.short_description = "Số lượng SIM"
    
    def goto_tag(self):  # new
        
        return mark_safe(f"""<a href="/sim-so-dep/{self.slug}" style="display: inline-block; padding: 7px 15px; border: none; border-radius: 5px; color: #fff; background-color: #47bac1; text-decoration: none; transition: all 0.3s ease;"
                         onmouseover="this.style.backgroundColor='#639af5'"
                            onmouseout="this.style.backgroundColor='#47bac1'"
  >
                Đi đến trang
                </a>""")
    goto_tag.short_description = ""
    
    def __str__(self):
        return self.name


class Network(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Tên nhà mạng')
    description = models.TextField(null=True, verbose_name='Mô tả', blank=True)
    image_logo = models.ImageField(upload_to='photos/networks', null=True, verbose_name='Logo nhà mạng:')
    image_simcard = models.ImageField(upload_to='photos/networks', null=True, verbose_name='Ảnh thẻ SIM:')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Ngày khởi tạo')

    def logo_preview(self):  # new
        return mark_safe(f'<img src = "{self.image_logo.url}" width = "50"/>')
    logo_preview.short_description = "Logo"

    def simcard_img_preview(self):  # new
        return mark_safe(f'<img src = "{self.image_simcard.url}" width = "200"/>')
    simcard_img_preview.short_description = "Ảnh thẻ SIM"
    
    def sim_count(self):
        return self.sims.count()
    sim_count.short_description = "Số lượng SIM khả dụng"

    def goto_net(self):  # new
        return mark_safe(f"""<a href="/nha-mang/{self.slug}" style="display: inline-block; padding: 7px 15px; border: none; border-radius: 5px; color: #fff; background-color: #47bac1; text-decoration: none; transition: all 0.3s ease;"
                         onmouseover="this.style.backgroundColor='#639af5'"
                            onmouseout="this.style.backgroundColor='#47bac1'"
  >
                Đi đến trang
                </a>""")
    goto_net.short_description = ""
    
    class Meta:
        verbose_name = 'Nhà mạng'
        verbose_name_plural  = "Danh sách nhà mạng"

    def __str__(self):
        return self.name


class SIM(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='Số điện thoại')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Giá')
    discount = models.PositiveIntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ], verbose_name='Giảm')
    description = models.TextField(verbose_name='Mô tả', null=True, blank=True)
    image = models.ImageField(upload_to='sim_images/', verbose_name='Ảnh SIM', null=True, blank=True)
    
    is_available = models.BooleanField(default=True, verbose_name='Khả thi')
    is_visible = models.BooleanField(default=True, verbose_name='Hiển thị')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    network = models.ForeignKey(
        Network, on_delete=models.CASCADE, related_name='sims', verbose_name='Nhà mạng')

    tags = models.ManyToManyField(
        Tag, related_name='sims', verbose_name='Loại SIM', blank=True)
    
    class Meta:
        verbose_name = 'SIM'
        verbose_name_plural  = "Danh sách SIM"

    def sim_img_preview(self):  # new
        return mark_safe(f'<img src = "{self.image.url}" width = "200"/>')
    sim_img_preview.short_description = "Ảnh thẻ SIM"

    def goto_sim(self):  # new
        return mark_safe(f"""<a href="/sim/{self.slug}" style="display: inline-block; padding: 7px 15px; border: none; border-radius: 5px; color: #fff; background-color: #47bac1; text-decoration: none; transition: all 0.3s ease;"
                         onmouseover="this.style.backgroundColor='#639af5'"
                            onmouseout="this.style.backgroundColor='#47bac1'"
  >
                Đi đến trang
                </a>""")
    goto_sim.short_description = ""
    
    def __str__(self):
        return self.phone_number

    def get_curr_price(self):
        new_price = self.price * (100 - self.discount) / 100
        return new_price
    get_curr_price.short_description = "Giá hiện tại"
    
    def get_salepricestr(self):
        new_price = self.price * (100 - self.discount) / 100
        return "{:,.0f}".format(new_price) + " đ"
    get_salepricestr.short_description = 'Giá giảm'

    def get_originalpricestr(self):
        return "{:,.0f}".format(self.price) + " đ"
    get_originalpricestr.short_description = 'Giá gốc'
    
    def get_tags(self):
        return ", ".join([t.name for t in self.tags.all()])
    get_tags.short_description = 'Loại SIM'
    
    def get_discount(self):
        return str(self.discount) + '%'
    get_discount.short_description = 'Giảm'

