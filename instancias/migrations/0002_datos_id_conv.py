# Generated by Django 5.0.4 on 2024-05-10 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instancias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datos',
            name='id_conv',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
