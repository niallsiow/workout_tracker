# Generated by Django 5.0.14 on 2025-04-11 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workouts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="session",
            name="notes",
            field=models.TextField(blank=True),
        ),
    ]
