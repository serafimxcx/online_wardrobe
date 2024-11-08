# Generated by Django 5.0.4 on 2024-04-21 15:29

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0017_useritem_datetime_alter_useraccount_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 21, 15, 29, 16, 692445, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='useritem',
            name='desc',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='UserOutfits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outfit_name', models.CharField(max_length=255)),
                ('desc', models.TextField(blank=True, max_length=500, null=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('c_bottom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bottom_outfits', to='wardrobe.useritem')),
                ('c_footwear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='footwear_outfits', to='wardrobe.useritem')),
                ('c_outerwear', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='outerwear_outfits', to='wardrobe.useritem')),
                ('c_top', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='top_outfits', to='wardrobe.useritem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wardrobe.useraccount')),
            ],
        ),
    ]
