# Generated by Django 5.0.4 on 2024-04-13 12:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0011_fashionitem_gendered_alter_useraccount_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pref_genderedstyle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 13, 12, 22, 57, 376189, tzinfo=datetime.timezone.utc)),
        ),
    ]
