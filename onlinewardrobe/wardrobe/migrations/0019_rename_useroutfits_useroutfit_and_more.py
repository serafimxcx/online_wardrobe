# Generated by Django 5.0.4 on 2024-04-21 15:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0018_alter_useraccount_date_joined_alter_useritem_desc_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserOutfits',
            new_name='UserOutfit',
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 21, 15, 38, 13, 96947, tzinfo=datetime.timezone.utc)),
        ),
    ]
