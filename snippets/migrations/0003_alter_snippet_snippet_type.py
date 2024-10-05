# Generated by Django 5.1.1 on 2024-10-05 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_snippet_snippet_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='snippet_type',
            field=models.CharField(choices=[('python', 'Python'), ('javascript', 'JavaScript'), ('java', 'Java'), ('c', 'C'), ('cpp', 'C++'), ('ruby', 'Ruby'), ('php', 'PHP'), ('html', 'HTML'), ('css', 'CSS'), ('go', 'Go'), ('swift', 'Swift')], max_length=15),
        ),
    ]
