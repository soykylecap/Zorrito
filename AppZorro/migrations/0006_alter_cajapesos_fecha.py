# Generated by Django 4.2 on 2024-08-11 02:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AppZorro", "0005_remove_rubros_tipo_alter_cajapesos_egreso_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cajapesos",
            name="fecha",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
