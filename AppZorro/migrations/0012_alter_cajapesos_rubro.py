# Generated by Django 4.2 on 2024-08-11 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("AppZorro", "0011_alter_cajapesos_rubro"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cajapesos",
            name="rubro",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="AppZorro.rubros",
            ),
        ),
    ]
