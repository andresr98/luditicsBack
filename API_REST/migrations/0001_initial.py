# Generated by Django 2.0.7 on 2018-09-13 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('grado', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=253)),
                ('contrasena', models.CharField(max_length=255)),
                ('tipo_documento', models.CharField(max_length=50)),
                ('numero_documento', models.CharField(max_length=30)),
                ('sexo_biologico', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='ProfesorXGrupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jornada', models.CharField(max_length=50, null=True)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_REST.Grupo')),
                ('profesor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='API_REST.Profesor')),
            ],
        ),
    ]