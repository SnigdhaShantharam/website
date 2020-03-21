# Generated by Django 2.2 on 2020-03-21 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accessories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('inventory', models.IntegerField()),
                ('ratings', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('image1', models.ImageField(blank=True, max_length=500, null=True, upload_to='media/equipments')),
                ('image2', models.ImageField(max_length=500, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('inventory', models.IntegerField()),
                ('ratings', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('image1', models.ImageField(blank=True, max_length=500, null=True, upload_to='media/equipments')),
                ('image2', models.ImageField(blank=True, max_length=500, null=True, upload_to='media/equipments')),
                ('image3', models.ImageField(blank=True, max_length=500, null=True, upload_to='media/equipments')),
                ('image4', models.ImageField(blank=True, max_length=500, null=True, upload_to='media/equipments')),
            ],
        ),
        migrations.CreateModel(
            name='Lens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('inventory', models.IntegerField()),
                ('ratings', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('image1', models.ImageField(blank=True, max_length=500, null=True, upload_to='media/equipments')),
                ('image2', models.ImageField(blank=True, max_length=500, null=True, upload_to='media/equipments')),
                ('image3', models.ImageField(blank=True, max_length=500, null=True, upload_to='media/equipments')),
                ('image4', models.ImageField(blank=True, max_length=500, null=True, upload_to='media/equipments')),
            ],
            options={
                'verbose_name': 'Lens',
                'verbose_name_plural': 'Lenses',
            },
        ),
    ]
