# Generated by Django 2.0.7 on 2018-09-24 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API_REST', '0009_auto_20180916_1246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoria',
            old_name='subcategoria',
            new_name='padre',
        ),
        migrations.AlterField(
            model_name='grupoxestudiante',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_REST.Estudiante'),
        ),
        migrations.AlterField(
            model_name='profesorxgrupo',
            name='profesor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_REST.Profesor'),
        ),
    ]
