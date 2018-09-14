# Generated by Django 2.0.7 on 2018-09-13 05:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('API_REST', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=75)),
                ('tipo', models.CharField(max_length=50)),
                ('icono', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('sexo_biologico', models.CharField(max_length=25)),
                ('descripcion', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstudianteXCategoria',
            fields=[
                ('fecha_asignacion', models.DateTimeField(default=django.utils.timezone.now, primary_key=True, serialize=False)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_REST.Categoria')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_REST.Estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='EstudianteXSubcategoria',
            fields=[
                ('fecha_asignacion', models.DateTimeField(default=django.utils.timezone.now, primary_key=True, serialize=False)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_REST.Estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='GrupoXEstudiante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estudiante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='API_REST.Estudiante')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_REST.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=75)),
                ('icono', models.CharField(max_length=255)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_REST.Categoria')),
            ],
        ),
        migrations.AddField(
            model_name='estudiantexsubcategoria',
            name='subcategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API_REST.Subcategoria'),
        ),
    ]