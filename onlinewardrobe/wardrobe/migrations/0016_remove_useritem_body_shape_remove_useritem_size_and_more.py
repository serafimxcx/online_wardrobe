# Generated by Django 5.0.4 on 2024-04-17 09:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0015_alter_useraccount_date_joined_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useritem',
            name='body_shape',
        ),
        migrations.RemoveField(
            model_name='useritem',
            name='size',
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 17, 9, 12, 19, 617827, tzinfo=datetime.timezone.utc)),
        ),
    ]