# Generated by Django 5.0.2 on 2024-03-18 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instancias', '0009_remove_convenio_logueo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convenio',
            name='banner',
        ),
    ]
