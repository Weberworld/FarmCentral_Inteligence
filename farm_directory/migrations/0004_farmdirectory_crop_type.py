# Generated by Django 4.2.9 on 2024-02-06 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_directory', '0003_alter_farmdirectory_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmdirectory',
            name='crop_type',
            field=models.CharField(max_length=20, null=True),
        ),
    ]