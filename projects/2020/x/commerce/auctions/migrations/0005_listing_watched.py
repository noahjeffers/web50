# Generated by Django 3.1 on 2020-08-18 20:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_listedby'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watched',
            field=models.ManyToManyField(blank=True, related_name='watching', to=settings.AUTH_USER_MODEL),
        ),
    ]
