# Generated by Django 3.1 on 2020-08-19 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_watched'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='openingBid',
        ),
        migrations.AddField(
            model_name='listing',
            name='currentbid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='currentbid', to='auctions.bids'),
            preserve_default=False,
        ),
    ]
