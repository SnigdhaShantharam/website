# Generated by Django 3.0.4 on 2020-03-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_alternative_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reference',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
