# Generated by Django 4.2 on 2024-08-31 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("AppZorro", "0020_cajadolares_conecta_pesos_alter_cajadolares_autor_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cajapesos",
            name="conecta_dolares",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="AppZorro.cajadolares",
            ),
        ),
        migrations.AlterField(
            model_name="cajadolares",
            name="cotiza",
            field=models.FloatField(default=1275),
        ),
        migrations.AlterField(
            model_name="cajapesos",
            name="valor_dolar",
            field=models.FloatField(default=1275),
        ),
    ]
