# Generated by Django 5.1.2 on 2024-10-26 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_event_user_task_user_taskboard_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
    ]