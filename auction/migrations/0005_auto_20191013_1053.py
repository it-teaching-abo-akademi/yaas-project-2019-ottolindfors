# Generated by Django 2.2.5 on 2019-10-13 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0004_auto_20191011_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionmodel',
            name='token',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='auctionmodel',
            name='deadline_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]