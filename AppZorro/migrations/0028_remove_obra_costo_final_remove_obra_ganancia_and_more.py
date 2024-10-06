# Generated by Django 4.2 on 2024-09-17 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AppZorro", "0027_tarea_autor"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="obra",
            name="costo_final",
        ),
        migrations.RemoveField(
            model_name="obra",
            name="ganancia",
        ),
        migrations.AlterField(
            model_name="cajadolares",
            name="cotiza",
            field=models.FloatField(default=1245),
        ),
        migrations.AlterField(
            model_name="cajapesos",
            name="cotiza",
            field=models.FloatField(default=1245),
        ),
    ]