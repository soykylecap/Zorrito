# Generated by Django 4.2 on 2024-08-28 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("AppZorro", "0018_obras_cajadolares_es_cambio_cajapesos_valor_dolar_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Obras",
            new_name="Obra",
        ),
        migrations.RenameModel(
            old_name="Tareas",
            new_name="Tarea",
        ),
    ]
