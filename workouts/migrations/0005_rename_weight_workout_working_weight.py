# Generated by Django 5.0.14 on 2025-04-15 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("workouts", "0004_exercise_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="workout",
            old_name="weight",
            new_name="working_weight",
        ),
    ]
