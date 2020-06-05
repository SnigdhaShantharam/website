# Generated by Django 3.0.4 on 2020-05-11 14:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0008_auto_20200416_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='inventory',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
