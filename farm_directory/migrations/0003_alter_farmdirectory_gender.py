# Generated by Django 4.2.9 on 2024-03-13 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_directory', '0002_alter_farmdirectory_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmdirectory',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default=None, max_length=6, null=True),
        ),
    ]