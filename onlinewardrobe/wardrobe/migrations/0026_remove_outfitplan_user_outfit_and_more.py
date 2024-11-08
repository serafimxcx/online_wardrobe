# Generated by Django 5.0.4 on 2024-05-09 05:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0025_rename_outfit_plan_outfitplan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outfitplan',
            name='user_outfit',
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 9, 5, 50, 26, 992272, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='outfitplan',
            name='user_outfit',
            field=models.ManyToManyField(blank=True, to='wardrobe.useroutfit'),
        ),
    ]
