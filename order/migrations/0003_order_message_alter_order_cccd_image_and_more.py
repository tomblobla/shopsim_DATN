# Generated by Django 4.1.7 on 2023-05-11 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_order_date_order_paid_date_order_ship_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='message',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Yêu cầu khách hàng'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cccd_image',
            field=models.ImageField(blank=True, null=True, upload_to='cccd_images/', verbose_name='Ảnh CCCD đăng ký'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Thời gian đặt'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('PENDING', 'Chuẩn bị tiếp nhận'), ('PROCESSING', 'Đang xử lý'), ('SHIPPING', 'Đang giao hàng'), ('DELIVERED', 'Đã giao hàng'), ('REFUNDED', 'Đã hoàn'), ('CANCELLED', 'Đã hủy')], max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='portrait_image',
            field=models.ImageField(blank=True, null=True, upload_to='portrait_images/', verbose_name='Ảnh chân dung đăng ký'),
        ),
    ]