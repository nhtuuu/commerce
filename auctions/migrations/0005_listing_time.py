# Generated by Django 3.2.12 on 2023-03-18 08:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20230318_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
    ]
