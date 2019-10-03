# Generated by Django 2.2.5 on 2019-10-03 09:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_auto_20191002_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionmodel',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 3, 12, 48, 17, 908342)),
        ),
        migrations.AddField(
            model_name='auctionmodel',
            name='minimum_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='auctionmodel',
            name='status',
            field=models.CharField(default='Active', max_length=1024),
        ),
    ]