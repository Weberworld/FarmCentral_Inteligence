# Generated by Django 4.2.9 on 2024-01-31 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_directory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmdirectory',
            name='bvn',
            field=models.SmallIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='farmdirectory',
            name='nin',
            field=models.SmallIntegerField(blank=True, null=True, unique=True),
        ),
    ]