# Generated by Django 4.2.9 on 2024-03-13 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_rename_temp_data_otp_signed_data_alter_otp_hash_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='account',
            name='profile_img',
            field=models.FileField(blank=True, null=True, upload_to='images'),
        ),
    ]
