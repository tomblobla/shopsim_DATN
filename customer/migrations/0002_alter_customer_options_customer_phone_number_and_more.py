# Generated by Django 4.1.7 on 2023-05-09 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Khách hàng', 'verbose_name_plural': 'Danh sách Khách hàng'},
        ),
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, unique=True, verbose_name='Số điện thoại'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=200, verbose_name='Địa chỉ'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='Địa chỉ email'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('M', 'Nam'), ('F', 'Nữ')], max_length=1, verbose_name='Giới tính'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Đang hoạt động'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='Là Admin'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Họ'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(max_length=30, unique=True, verbose_name='Tên đăng nhập'),
        ),
    ]
