# Generated by Django 3.0.4 on 2020-04-16 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_auto_20200416_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='inventory',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
