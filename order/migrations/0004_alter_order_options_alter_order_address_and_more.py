# Generated by Django 4.1.7 on 2023-05-12 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sim_manager', '0001_initial'),
        ('order', '0003_order_message_alter_order_cccd_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Đơn hàng', 'verbose_name_plural': 'Danh sách đơn hàng'},
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=250, verbose_name='Địa chỉ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Enail'),
        ),
        migrations.AlterField(
            model_name='order',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='Họ và tên'),
        ),
        migrations.AlterField(
            model_name='order',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Nam'), ('F', 'Nữ')], max_length=1, null=True, verbose_name='Giới tính'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Trạng thái thanh toán'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('PENDING', 'Chuẩn bị tiếp nhận'), ('PROCESSING', 'Đang xử lý'), ('SHIPPING', 'Đang giao hàng'), ('DELIVERED', 'Đã giao hàng'), ('REFUNDED', 'Đã hoàn'), ('CANCELLED', 'Đã hủy')], max_length=20, verbose_name='Trạng thái đơn'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paid_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Ngày thanh toán'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('COD', 'Trả tiền khi nhận hàng'), ('TRANSFER', 'Chuyển khoản')], max_length=10, verbose_name='Phương thức thanh toán'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=20, verbose_name='Số điện thoại'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ship_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Ngày giao hàng'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_provider',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nhà vận chuyển'),
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Mã đơn vận'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order', verbose_name='Sim'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='sim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='sim_manager.sim', verbose_name='Sim'),
        ),
    ]
