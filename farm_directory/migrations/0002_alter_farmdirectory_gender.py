# Generated by Django 4.2.9 on 2024-03-13 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_directory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmdirectory',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default=None, max_length=6),
        ),
    ]