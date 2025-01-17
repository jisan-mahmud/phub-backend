# Generated by Django 5.1.1 on 2024-11-18 02:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_follow_followed'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('followed', 'follower')},
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(condition=models.Q(('followed', models.F('follower')), _negated=True), name='prevent_self_follow'),
        ),
    ]
