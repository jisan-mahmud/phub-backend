# Generated by Django 5.1.1 on 2024-10-04 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_followers_customuser_following_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
