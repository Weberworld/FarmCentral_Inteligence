# Generated by Django 4.2.9 on 2024-01-31 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_directory', '0002_alter_farmdirectory_bvn_alter_farmdirectory_nin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmdirectory',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6),
        ),
    ]