# Generated by Django 3.0.4 on 2020-04-15 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_auto_20200415_1216'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.RemoveField(
            model_name='event',
            name='inventory',
        ),
    ]
