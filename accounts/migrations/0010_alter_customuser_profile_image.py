# Generated by Django 5.1.1 on 2024-11-27 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(default='../phub_backend/media/profile/profile/profile_avatar.jpg', upload_to='profile/'),
        ),
    ]
