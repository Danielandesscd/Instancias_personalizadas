# Generated by Django 5.0.4 on 2024-04-25 02:17

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CONVENIO',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('certificados_permi', models.CharField(max_length=100)),
                ('o_cert_permi', models.CharField(max_length=100)),
                ('o_firmado_permi', models.CharField(max_length=100)),
                ('o_otp_permi', models.CharField(max_length=100)),
                ('vigencias_permi', models.CharField(max_length=100)),
                ('formatos_entrega_permi', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100, null=True)),
                ('color_primario', models.CharField(max_length=100)),
                ('color_secundario', models.CharField(max_length=100)),
                ('id_vigenica', models.IntegerField(null=True)),
                ('imagen_banner', models.ImageField(blank=True, null=True, upload_to='banners/')),
                ('contraseña_convenio', models.TextField(blank=True, null=True)),
                ('usuario_weservice', models.CharField(max_length=100, null=True)),
                ('contraseña_webservice', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DATOS',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('tipo_doc', models.CharField(max_length=100)),
                ('nuemro_doc', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('departamento', models.CharField(max_length=100)),
                ('municipio', models.CharField(max_length=100)),
                ('documentos', models.CharField(max_length=100)),
                ('ocupacion', models.CharField(max_length=100)),
                ('cargo', models.CharField(max_length=100)),
                ('unidad_organizacional', models.CharField(max_length=100)),
                ('token_andesid', models.CharField(max_length=100)),
                ('universidad', models.CharField(max_length=100)),
                ('facultad', models.CharField(max_length=100)),
                ('titulo_profesional', models.CharField(max_length=100)),
                ('matricula_profesional', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FORMATO_ENTREGA',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_convenio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FormatoEntrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OperacionCertificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OperacionFirmado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OperacionOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SOLICITUD_CERT',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_certificado', models.IntegerField()),
                ('id_convenio', models.IntegerField()),
                ('id_datos', models.IntegerField()),
                ('nombre_cert', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TIPO_CERT',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_cert', models.CharField(max_length=100)),
                ('id_convenio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoCertificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VIGENCIA',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_cert', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VigenciaCertificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duracion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CONFI_CERTIFICADOS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_certificado', models.CharField(max_length=255)),
                ('vigencias', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('formatos', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None)),
                ('id_convenio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instancias.convenio')),
            ],
        ),
        migrations.AddField(
            model_name='convenio',
            name='formatos_entrega',
            field=models.ManyToManyField(related_name='convenios', to='instancias.formatoentrega'),
        ),
        migrations.AddField(
            model_name='convenio',
            name='operaciones_certificado',
            field=models.ManyToManyField(related_name='convenios', to='instancias.operacioncertificado'),
        ),
        migrations.AddField(
            model_name='convenio',
            name='operaciones_firmado',
            field=models.ManyToManyField(related_name='convenios', to='instancias.operacionfirmado'),
        ),
        migrations.AddField(
            model_name='convenio',
            name='operaciones_otp',
            field=models.ManyToManyField(related_name='convenios', to='instancias.operacionotp'),
        ),
        migrations.AddField(
            model_name='convenio',
            name='certificados_seleccionados',
            field=models.ManyToManyField(related_name='convenios', to='instancias.tipo_cert'),
        ),
        migrations.AddField(
            model_name='convenio',
            name='tipos_certificado',
            field=models.ManyToManyField(related_name='convenios', to='instancias.tipocertificado'),
        ),
        migrations.AddField(
            model_name='convenio',
            name='vigencias_certificado',
            field=models.ManyToManyField(related_name='convenios', to='instancias.vigenciacertificado'),
        ),
    ]
