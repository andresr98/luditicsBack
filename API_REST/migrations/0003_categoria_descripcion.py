# Generated by Django 2.0.7 on 2018-09-29 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_REST', '0002_auto_20180924_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='descripcion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]