# Generated by Django 4.1.7 on 2023-03-08 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sim',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Giá'),
        ),
    ]