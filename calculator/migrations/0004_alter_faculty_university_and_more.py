# Generated by Django 5.1.1 on 2024-11-12 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0003_studentexamscore"),
    ]

    operations = [
        migrations.AlterField(
            model_name="faculty",
            name="university",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="calculator.university"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="faculty",
            unique_together={("university", "name")},
        ),
    ]
