from django.db import models
from django.utils import timezone

class DATOS (models.Model):
    id= models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    tipo_certificado = models.CharField(max_length=100)
    formato_entrega = models.CharField(max_length=50)
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
    
    def _str_(self):
        return self.DATOS
    
class SOLICITUD_CERT (models.Model):
    id= models.AutoField(primary_key=True)
    id_certificado = models.IntegerField(primary_key=True)
    id_convenio = models.IntegerField(primary_key=True)
    id_datos = models.IntegerField(primary_key=True)
    nombre_cert = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)

    def _str_(self):
        return self.SOLICITUD_CERT
    
class CONVENIO (models.Model):
    id= models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    logueo = models.BooleanField(max_length=100)
    logo = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    color_primario = models.CharField(max_length=100)
    color_secundario = models.CharField(max_length=100)
    id_vigenica = models.IntegerField(primary_key=True)
    banner = models.BooleanField(max_length=100)
    usuario_weservice = models.CharField(max_length=100)
    contraseña_webservice = models.CharField(max_length=100)

    def _str_(self):
        return self.CONVENIO
    
class TIPO_CERT (models.Model):
    id= models.AutoField(primary_key=True)
    nombre_cert = models.CharField(max_length=100)
    id_formulario = models.IntegerFieldField(max_length=100)
    id_convenio = models.IntegerFieldField(max_length=100)

    def _str_(self):
        return self.TIPO_CERT
    
class FORMATO_ENTREGA (models.Model):
    id= models.AutoField(primary_key=True)
    token_virtual= models.CharField(primary_key=True)
    token_integer= models.CharField(primary_key=True)
    pkcs10= models.CharField(primary_key=True)
    id_convenio= models.IntegerField(primary_key=True)
    
    def _str_(self):
        return self.FORMATO_ENTREGA
    
class VIGENCIA (models.Model):
    id= models.AutoField(primary_key=True)
    id_cert= models.IntegerField(primary_key=True)

    def _str_(self):
        return self.VIGENCIA