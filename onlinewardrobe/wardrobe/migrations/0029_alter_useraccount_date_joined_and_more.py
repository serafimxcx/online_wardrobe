# Generated by Django 5.0.4 on 2024-05-22 01:33

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0028_useroutfit_dress_alter_useraccount_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 22, 1, 33, 25, 18926, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='useroutfit',
            name='bottom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bottom_outfits', to='wardrobe.useritem'),
        ),
    ]