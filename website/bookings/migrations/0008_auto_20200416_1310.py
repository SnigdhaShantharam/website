# Generated by Django 3.0.4 on 2020-04-16 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0007_event_inventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='inventory',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
