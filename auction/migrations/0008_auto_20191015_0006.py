# Generated by Django 2.2.5 on 2019-10-14 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0007_auto_20191014_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionmodel',
            name='minimum_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='bidmodel',
            name='new_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]
