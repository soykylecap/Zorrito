# Generated by Django 4.2 on 2024-09-19 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AppZorro", "0028_remove_obra_costo_final_remove_obra_ganancia_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="obra",
            name="dias_final",
        ),
        migrations.AlterField(
            model_name="cajadolares",
            name="cotiza",
            field=models.FloatField(default=1230),
        ),
        migrations.AlterField(
            model_name="cajapesos",
            name="cotiza",
            field=models.FloatField(default=1230),
        ),
    ]