# Generated by Django 2.0.7 on 2018-10-23 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_REST', '0013_auto_20181013_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesorxgrupo',
            name='columnas',
            field=models.PositiveIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='profesorxgrupo',
            name='filas',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
