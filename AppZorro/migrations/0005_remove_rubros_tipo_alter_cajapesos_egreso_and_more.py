# Generated by Django 4.2 on 2024-08-10 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "AppZorro",
            "0004_alter_cajapesos_comprobante_alter_cajapesos_egreso_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rubros",
            name="tipo",
        ),
        migrations.AlterField(
            model_name="cajapesos",
            name="egreso",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="cajapesos",
            name="ingreso",
            field=models.FloatField(default=0),
        ),
    ]