# Generated by Django 3.1 on 2020-08-19 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20200819_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='currentbid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='currentbid', to='auctions.bids'),
        ),
    ]
