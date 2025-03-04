# Generated by Django 5.1.1 on 2024-10-07 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0003_alter_snippet_snippet_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snippet',
            old_name='snippet_type',
            new_name='language',
        ),
        migrations.AddField(
            model_name='snippet',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private'), ('unlisted', 'Unlisted')], default='public', max_length=10),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='explanation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
