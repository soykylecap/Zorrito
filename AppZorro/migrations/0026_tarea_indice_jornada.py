# Generated by Django 4.2 on 2024-09-15 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AppZorro", "0025_tarea_rubro_alter_cajadolares_cotiza_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tarea",
            name="indice_jornada",
            field=models.FloatField(default=1),
        ),
    ]
