# Generated by Django 5.0.3 on 2024-03-16 09:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0006_rename_itemcategories_itemcategory_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyShape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 16, 9, 10, 20, 199475, tzinfo=datetime.timezone.utc)),
        ),
    ]
