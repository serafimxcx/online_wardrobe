# Generated by Django 5.0.4 on 2024-05-17 00:12

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0027_remove_fashionitem_user_save_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useroutfit',
            name='dress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dress_outfits', to='wardrobe.useritem'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 17, 0, 12, 50, 8588, tzinfo=datetime.timezone.utc)),
        ),
    ]
