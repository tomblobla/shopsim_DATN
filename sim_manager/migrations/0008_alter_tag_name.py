# Generated by Django 4.1.7 on 2023-03-19 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim_manager', '0007_alter_network_image_logo_alter_network_image_simcard_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Loại SIM'),
        ),
    ]
