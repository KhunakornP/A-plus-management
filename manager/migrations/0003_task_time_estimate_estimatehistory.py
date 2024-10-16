# Generated by Django 5.1.1 on 2024-10-14 08:40

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0002_event"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="time_estimate",
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name="EstimateHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.localdate)),
                ("time_remaining", models.IntegerField(default=0)),
                (
                    "taskboard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="manager.taskboard",
                    ),
                ),
            ],
        ),
    ]
