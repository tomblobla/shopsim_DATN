# Generated by Django 4.1.7 on 2023-03-19 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim_manager', '0009_alter_sim_description_alter_sim_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sim',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='sims', to='sim_manager.tag', verbose_name='Loại SIM'),
        ),
    ]
