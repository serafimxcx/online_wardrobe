# Generated by Django 5.0.4 on 2024-05-09 02:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0024_alter_useraccount_date_joined_outfit_plan'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Outfit_Plan',
            new_name='OutfitPlan',
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 9, 2, 54, 58, 454383, tzinfo=datetime.timezone.utc)),
        ),
    ]
