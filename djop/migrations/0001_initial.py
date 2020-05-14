from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectPermission',
            fields=[(
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'),
                ), (
                    'object_id',
                    models.TextField(verbose_name='object id'),
                ), (
                    'groups',
                    models.ManyToManyField(
                        related_name='object_permissions',
                        to='auth.Group',
                        verbose_name='groups'),
                ), (
                    'permission',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='auth.Permission', verbose_name='permission'),
                ), (
                    'users',
                    models.ManyToManyField(
                        related_name='object_permissions',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='users'),
            )],
        ),
        migrations.AlterUniqueTogether(
            name='objectpermission',
            unique_together={('permission', 'object_id')},
        ),
    ]
