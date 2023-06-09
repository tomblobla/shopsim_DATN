# Generated by Django 4.1.7 on 2023-05-10 15:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sim_manager', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='paid_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='ship_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='order.order', verbose_name='Sim')),
                ('sim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='sim_manager.sim', verbose_name='Sim')),
            ],
            options={
                'verbose_name': 'Sim',
                'verbose_name_plural': 'Danh sách SIM',
                'unique_together': {('sim', 'order')},
            },
        ),
    ]
