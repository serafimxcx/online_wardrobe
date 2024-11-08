# Generated by Django 5.0.3 on 2024-03-16 08:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0003_itemcolor_itemstyle_alter_useraccount_date_joined'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 16, 8, 54, 43, 372156, tzinfo=datetime.timezone.utc)),
        ),
    ]
