# Generated by Django 5.0.4 on 2024-05-25 06:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0031_fashionitem_brand_fashionitem_item_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 25, 6, 12, 17, 122868, tzinfo=datetime.timezone.utc)),
        ),
    ]
