# Generated by Django 4.2 on 2024-08-28 00:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("AppZorro", "0017_cajadolares"),
    ]

    operations = [
        migrations.CreateModel(
            name="Obras",
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
                ("fecha_inicio", models.DateField(default=datetime.date.today)),
                ("nombre", models.CharField(max_length=30)),
                ("m2_cubiertos", models.FloatField(default=0.0)),
                ("m2_semicubiertos", models.FloatField(default=0.0)),
                ("m2_total", models.FloatField(default=0.0)),
                ("dias_estimados", models.IntegerField(default=30)),
                ("dias_final", models.IntegerField(default=0)),
                ("presupuesto_inicial", models.FloatField()),
                ("costo_final", models.FloatField()),
                ("ganancia", models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name="cajadolares",
            name="es_cambio",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="cajapesos",
            name="valor_dolar",
            field=models.FloatField(default=1310),
        ),
        migrations.CreateModel(
            name="Tareas",
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
                ("fecha", models.DateTimeField(default=datetime.date.today)),
                ("tarea", models.CharField(max_length=40)),
                (
                    "porcentaje",
                    models.IntegerField(
                        choices=[(25, "25%"), (50, "50%"), (75, "75%"), (100, "100%")],
                        default=100,
                    ),
                ),
                ("cant_operarios", models.IntegerField(default=2)),
                (
                    "obra",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="AppZorro.obras",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cajadolares",
            name="obra",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="AppZorro.obras",
            ),
        ),
        migrations.AddField(
            model_name="cajapesos",
            name="obra",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="AppZorro.obras",
            ),
        ),
    ]
