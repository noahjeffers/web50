# Generated by Django 3.1 on 2020-08-18 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_comments_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageLink',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]
