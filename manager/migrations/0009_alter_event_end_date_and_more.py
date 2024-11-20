# Generated by Django 5.1.2 on 2024-11-08 16:01

import manager.models.functions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_remove_task_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(default=manager.models.functions.today_midnight, verbose_name='End date'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(condition=models.Q(('end_date__gt', models.F('start_date'))), name='end_date must be greater than start_date'),
        ),
    ]