# Generated by Django 4.0.6 on 2022-09-06 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0002_alter_cuadrillatecnicamodel_table_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodoeventoequipoafectadomodel',
            name='eventid',
        ),
        migrations.AddField(
            model_name='nodoeventoequipoafectadomodel',
            name='evento',
            field=models.ForeignKey(default=7840, on_delete=django.db.models.deletion.CASCADE, to='metrics.nodoeventomodel'),
            preserve_default=False,
        ),
    ]