# Generated by Django 2.2.5 on 2019-10-02 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionmodel',
            old_name='body',
            new_name='description',
        ),
    ]
