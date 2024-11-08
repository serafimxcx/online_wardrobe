# Generated by Django 5.0.4 on 2024-05-25 06:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0030_useroutfit_accessories_alter_useraccount_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='fashionitem',
            name='brand',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='fashionitem',
            name='item_link',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 25, 6, 10, 44, 752969, tzinfo=datetime.timezone.utc)),
        ),
    ]