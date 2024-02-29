from django.db import models
from django.utils import timezone

class DATOS(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    tipo_certificado = models.CharField(max_length=100)
    formato_entrega = models.CharField(max_length=100)
    vigencia = models.CharField(max_length=100)
    documentos = models.CharField(max_length=100)
    ocupacion = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    unidad_organizacional = models.CharField(max_length=100)
    token_andesid = models.CharField(max_length=100)
    universidad = models.CharField(max_length=100)
    facultad = models.CharField(max_length=100)
    titulo_profesional = models.CharField(max_length=100)
    matricula_profesional = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)

    
    
class SOLICITUD_CERT(models.Model):
    id = models.AutoField(primary_key=True)
    id_certificado = models.IntegerField()
    id_convenio = models.IntegerField()
    id_datos = models.IntegerField()
    nombre_cert = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)



    
class CONVENIO(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    logueo = models.BooleanField()
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    url = models.CharField(max_length=100, null=True)
    color_primario = models.CharField(max_length=100)
    color_secundario = models.CharField(max_length=100)
    id_vigenica = models.IntegerField( null=True)
    banner = models.BooleanField()
    imagen_banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    usuario_weservice = models.CharField(max_length=100, null=True)
    contraseña_webservice = models.CharField(max_length=100, null=True)


    
    
class TIPO_CERT(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_cert = models.CharField(max_length=100)
    id_formulario = models.IntegerField()
    id_convenio = models.IntegerField()


    
    
class FORMATO_ENTREGA(models.Model):
    id = models.AutoField(primary_key=True)
    token_virtual = models.CharField(max_length=100)
    token_integer = models.CharField(max_length=100)
    pkcs10 = models.CharField(max_length=100)
    id_convenio = models.IntegerField()

    
 
    
class VIGENCIA(models.Model):
    id = models.AutoField(primary_key=True)
    id_cert = models.IntegerField()


    