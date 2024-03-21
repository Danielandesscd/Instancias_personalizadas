from http import client
from django.shortcuts import render, redirect
from suds.client import Client
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CONVENIO, TIPO_CERT
from django.contrib.auth.hashers import make_password
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import json
from django.conf import settings

from django.http import JsonResponse
from django.utils.encoding import force_str

from django.views.decorators.csrf import csrf_exempt

import requests
from requests import Session

import xml.etree.ElementTree as ET
import base64
from zeep import Client, Transport
from zeep.exceptions import TransportError, XMLSyntaxError

from zeep.wsse.username import UsernameToken
from django.shortcuts import render, get_object_or_404


def inicio(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('contraseña')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            return redirect('home')
        else:
            
            return render(request, 'inicio.html', {'error': 'Usuario o contraseña incorrectos'})
    else:

        return render(request, 'inicio.html')
    


def detalle_convenio(request, convenio_id):
    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    return render(request, 'plantilla_convenio.html', {'convenio': convenio})



def home(request):
    convenios = CONVENIO.objects.all().values_list('nombre', flat=True)
    convenios_text = [force_str(nombre) for nombre in convenios]
    print("convenios:", convenios_text)  
    return render(request, 'home.html', {'convenios': convenios_text})

def consultar(request):
    return render (request, 'consultar_cert.html')

def revocar(request):
    return render (request, 'revocar_cert.html')

def cambiar_pin(request):
    return render (request, 'cambiar_pin.html')

def firmar_doc(request):
    return render (request, 'firmar_documento.html')

def campos_form(request):
    return render(request,'campos-form.html')


def instancia(request):
    return render (request, 'instancia.html')

def certificado_perso_nat(request):
    return render (request, 'form-pers-nat.html')

def certificado_perso_jur(request):
    return render (request, 'form-pers-jur.html')

def certificado_perso_nat_rut(request):
    return render (request, 'form-per-nat-rut.html')

def certificado_pert_emp(request):
    return render (request, 'form-pert-emp.html')

def certificado_prof_titu(request):
    return render (request, 'form-prof-titu.html')

def certificado_fact_pj(request):
    return render (request, 'form-fe-pj.html')

def certificado_fact_pn(request):
    return render (request, 'form-fe-pn.html')


def procesar_formulario_convenio(request):
    if request.method == 'POST':
        # Procesar el formulario para crear una nueva instancia de CONVENIO
        convenio = CONVENIO(nombre=request.POST['nombre'])
        convenio.save()
        
        # Obtener los certificados seleccionados del formulario
        certificados_seleccionados_ids = request.POST.getlist('tipos_certificados')
        
        # Asociar los certificados seleccionados con el convenio creado
        for certificado_id in certificados_seleccionados_ids:
            TIPO_CERT = TIPO_CERT.objects.get(pk=certificado_id)
            convenio.certificados_seleccionados.add(TIPO_CERT)
        
        return render(request, 'tu_template.html', {'convenio': convenio})
    else:
        return render(request, 'tu_formulario.html')



@csrf_exempt
def guardar_convenios(request):
    if request.method == 'POST':
        data = request.POST.dict()

        # Obtener los IDs de los certificados seleccionados
        certificados_seleccionados = [key for key, value in data.items() if value == 'on']

        # Convertir la lista de IDs en una cadena separada por comas
        certificados_permi = ','.join(certificados_seleccionados)

        # Crear una nueva instancia de Convenio y guardarla en la base de datos
        convenio = CONVENIO(certificados_permi=certificados_permi)
        convenio.save()

        return JsonResponse({'message': 'Convenios guardados correctamente.'})

    return JsonResponse({'error': 'Se esperaba una solicitud POST.'}, status=400)

@csrf_exempt
def crear_instancia(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        logo = request.FILES.get('logo')
        url = request.POST.get('url')
        color_primario = request.POST.get('colorPrimario')
        color_secundario = request.POST.get('colorSecundario')
        id_vigenica = request.POST.get('id_vigenica')
        imagen_banner = request.FILES.get('imagenBanner')
        usuario_weservice = request.POST.get('usuario_weservice')
        contraseña_webservice = request.POST.get('contraseña_webservice')
        contraseña_convenio = request.POST.get('contraseña')

        contraseña_convenio_encriptada = make_password(contraseña_convenio)
        print("Contenido de request.POST:", request.POST)

        # Obtener los certificados seleccionados
        certificado_persona_natural = request.POST.get('certificado_persona_natural')
        certificado_persona_juridica = request.POST.get('certificado_persona_juridica')
        certificado_pertenencia_empresa = request.POST.get('certificado_pertenencia_empresa')
        certificado_Comunidada_Académica = request.POST.get('certificado_Comunidada_Académica')
        certificado_Función_Publica_SIIF_Nación = request.POST.get('certificado_Función_Publica_SIIF_Nación')
        certificado_Profesional_Titulado  = request.POST.get('certificado_Profesional_Titulado ')
        certificado_Persona_Natural_Con_RUT = request.POST.get('certificado_Persona_Natural_Con_RUT')
        certificado_Facturacion_Electronica_Persona_JurÍdica = request.POST.get('certificado_Facturacion_Electronica_Persona_JurÍdica')
        certificado_Facturacion_Electronica_Persona_Natural = request.POST.get('certificado_Facturacion_Electronica_Persona_Natural')
        certificado_Funcion_Publica = request.POST.get('certificado_Funcion_Publica')
        certificado_Representante_Legal = request.POST.get('certificado_Representante_Legal')

        # Obtener las operaciones de certificado seleccionadas
        consultar_certificado = request.POST.get('consultar_certificado')
        revocar_certificado = request.POST.get('revocar_certificado')
        cambiar_pin = request.POST.get('cambiar_pin')
        reposicion_certificado = request.POST.get('reposicion_certificado')
        
        # Obtener las operaciones de firmado seleccionadas
        firmar_documento = request.POST.get('firmar_documento')
        verificar_firma = request.POST.get('verificar_firma')
        
        # Obtener las operaciones de OTP seleccionadas
        cambiar_otp = request.POST.get('cambiar_otp')
        firmar_con_otp = request.POST.get('firmar_con_otp')
        invalidar_otp = request.POST.get('invalidar_otp')
        
        # Obtener las vigencias del certificado seleccionadas
        vigencia_1_dia = request.POST.get('vigencia_1_dia')
        vigencia_1_mes = request.POST.get('vigencia_1_mes')
        vigencia_3_meses = request.POST.get('vigencia_3_meses')
        vigencia_6_meses = request.POST.get('vigencia_6_meses')
        vigencia_1_ano = request.POST.get('vigencia_1_ano')
        vigencia_18_meses = request.POST.get('vigencia_18_meses')
        vigencia_2_anos = request.POST.get('vigencia_2_anos')
        
        # Obtener los formatos de entrega seleccionados
        token_virtual = request.POST.get('token_virtual')
        token_fisico = request.POST.get('token_fisico')
        pkcs10 = request.POST.get('pkcs10')



        # Concatenar los valores de los certificados
        certificados_permi = ','.join(filter(None, [ certificado_Representante_Legal,certificado_Funcion_Publica ,certificado_Funcion_Publica,certificado_Facturacion_Electronica_Persona_JurÍdica,certificado_Facturacion_Electronica_Persona_Natural,certificado_Persona_Natural_Con_RUT,certificado_Profesional_Titulado ,certificado_Función_Publica_SIIF_Nación,certificado_Comunidada_Académica,certificado_persona_natural, certificado_persona_juridica, certificado_pertenencia_empresa]))
        print("Certificados permiso:", certificados_permi)  # Imprimir en la terminal
        # Concatenar los valores de las operaciones de certificado
        o_cert_permi = ','.join(filter(None, [consultar_certificado, revocar_certificado, cambiar_pin, reposicion_certificado]))
        
        # Concatenar los valores de las operaciones de firmado
        o_firmado_permi = ','.join(filter(None, [firmar_documento, verificar_firma]))
        
        # Concatenar los valores de las operaciones de OTP
        o_otp_permi = ','.join(filter(None, [cambiar_otp, firmar_con_otp, invalidar_otp]))
        
        # Concatenar los valores de las vigencias del certificado
        vigencias_permi = ','.join(filter(None, [vigencia_1_dia, vigencia_1_mes, vigencia_3_meses, vigencia_6_meses, vigencia_1_ano, vigencia_18_meses, vigencia_2_anos]))
        
        # Concatenar los valores de los formatos de entrega
        formatos_entrega_permi = ','.join(filter(None, [token_virtual, token_fisico, pkcs10]))

        convenio = CONVENIO.objects.create(
            nombre=nombre,
            logo=logo,
            url=url,
            color_primario=color_primario,
            color_secundario=color_secundario,
            id_vigenica=id_vigenica,
            imagen_banner=imagen_banner,
            contraseña_convenio=contraseña_convenio_encriptada,
            usuario_weservice=usuario_weservice,
            contraseña_webservice=contraseña_webservice,
            certificados_permi=certificados_permi,
            o_cert_permi=o_cert_permi,
            o_firmado_permi=o_firmado_permi,
            o_otp_permi=o_otp_permi,
            vigencias_permi=vigencias_permi,
            formatos_entrega_permi=formatos_entrega_permi,
        )

        convenio.save()
        return redirect('home')
    return render(request, 'home.html')

def formulario_instancia(request):
    return render(request, 'formulario.html')

def campos_form(request):
    departamentos = obtener_departamentos()
    print("departamentos:", departamentos)  # Imprimirá los departamentos en la terminal
    return render(request, 'campos-form.html', {'departamentos': departamentos})

def obtener_departamentos():
    url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"

    payload = """
    <soapenv:Envelope xmlns:and="http://www.andesscd.com.co/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
       <soapenv:Header><wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"><wsse:UsernameToken wsu:Id="UsernameToken-7967B371AB1C77594517104219622713"><wsse:Username>PAAN</wsse:Username><wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">WEJdNHmFGnOeCnqNc/vIXRyJafs=</wsse:Password><wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">+fJQ1IEmt2xbAZooSaCNew==</wsse:Nonce><wsu:Created>2024-03-14T13:12:42.268Z</wsu:Created></wsse:UsernameToken></wsse:Security></soapenv:Header>
       <soapenv:Body>
          <and:DepartamentoRequest>
             <and:cadena/>
          </and:DepartamentoRequest>
       </soapenv:Body>
    </soapenv:Envelope>
    """

    headers = {
      'Content-Type': 'text/xml'
    }

    try:
        # Realiza la solicitud SOAP
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Lanza una excepción si la solicitud falla (por ejemplo, código de estado HTTP diferente de 200)
        
        # Analiza la respuesta XML para obtener los departamentos
        root = ET.fromstring(response.content)
        mensaje = root.find(".//{http://www.andesscd.com.co/}mensaje").text
        departamentos = json.loads(mensaje)
        
        # Devuelve los departamentos obtenidos de la respuesta SOAP
        return departamentos
    
    except requests.exceptions.RequestException as e:
        # Manejo de errores en caso de fallo de la solicitud SOAP
        return {'error': str(e)}
    


def obtener_municipios(id_departamento):
    url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"

    payload = """
    <soapenv:Envelope xmlns:and="http://www.andesscd.com.co/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
       <soapenv:Header/>
       <soapenv:Body>
          <and:MunicipioRequest>
             <and:id_departamento>%s</and:id_departamento>
          </and:MunicipioRequest>
       </soapenv:Body>
    </soapenv:Envelope>
    """ % id_departamento

    headers = {
      'Content-Type': 'text/xml',
      'Authorization': 'Basic UEFBTjpnTjlGMnVla3Ru'
    }

    try:
        # Realiza la solicitud SOAP
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Lanza una excepción si la solicitud falla (por ejemplo, código de estado HTTP diferente de 200)
        
        # Analiza la respuesta XML para obtener los municipios
        root = ET.fromstring(response.content)
        municipios = []
        print("municipios:",root)
        print("print:",response)

        for municipio in root.findall('.//and:Municipio', namespaces={'and': 'http://www.andesscd.com.co/'}):
            id_municipio = municipio.find('.//and:id_municipio', namespaces={'and': 'http://www.andesscd.com.co/'}).text
            nombre = municipio.find('.//and:nombre', namespaces={'and': 'http://www.andesscd.com.co/'}).text
            municipios.append({'id': id_municipio, 'nombre': nombre})
        
        # Devuelve los municipios obtenidos de la respuesta SOAP
        return municipios
    
    except requests.exceptions.RequestException as e:
        # Manejo de errores en caso de fallo de la solicitud SOAP
        return [{'error': str(e)}]

def obtener_municipios_ajax(request):
    if request.method == 'GET' and 'id_departamento' in request.GET:
        id_departamento = request.GET['id_departamento']
        municipios = obtener_municipios(id_departamento)
        return JsonResponse({'municipios': municipios})
    return JsonResponse({'error': 'Método de solicitud no permitido o falta el parámetro id_departamento'}, status=400)


def actualizacion_pkcs10(pkcs10, serial, pinso, pin, idsolicitud):
    url_servicio = 'https://ra.andesscd.com.co/test/WebService/soap-server_new.php?wsdl'
    client = Client(url_servicio)
    resultado = client.service.ActualizarPKCS10Request(pkcs10=pkcs10, serial=serial, pinso=pinso, pin=pin, idsolicitud=idsolicitud)
    return resultado

def cambio_pin(tipo_doc, documento, pinactual, pinnuevo):
    url_servicio = 'https://ra.andesscd.com.co/test/WebService/soap-server_new.php?wsdl'
    client = Client(url_servicio)
    resultado = client.service.CambiarPinRequest(tipoDoc=tipo_doc, documento=documento, pinactual=pinactual, pinnuevo=pinnuevo)
    return resultado


def certificado_facturacion_electronica(tipo_cert, tipo_doc, documento, nombres, apellidos, municipio, direccion, email, email_ent, telefono, celular, ocupacion, tipo_doc_ent, documento_ent, razonsocial, municipio_ent, direccion_ent, cargo, unidad_organizacional, organizacion_factel, fecha_cert, formato, vigencia_cert, testigo, foto, pin, pkcs10, soporte, verific_doc, plantilla_huella, token_andesid):
    url_servicio = 'https://ra.andesscd.com.co/test/WebService/soap-server_new.php?wsdl'
    client = Client(url_servicio)
    resultado = client.service.CertificadoFacturacionElectronicaRequest(tipoCert=tipo_cert, tipoDoc=tipo_doc, documento=documento, nombres=nombres, apellidos=apellidos, municipio=municipio, direccion=direccion, email=email, emailEnt=email_ent, telefono=telefono, celular=celular, ocupacion=ocupacion, tipoDocEnt=tipo_doc_ent, documentoEnt=documento_ent, razonsocial=razonsocial, municipioEnt=municipio_ent, direccionEnt=direccion_ent, cargo=cargo, unidadOrganizacional=unidad_organizacional, organizacionFactel=organizacion_factel, fechaCert=fecha_cert, formato=formato, vigenciaCert=vigencia_cert, testigo=testigo, foto=foto, pin=pin, pkcs10=pkcs10, soporte=soporte, verific_doc=verific_doc, plantillaHuella=plantilla_huella, token_andesid=token_andesid)
    return resultado


def certificado_facturacion_electronica_con_fecha(tipo_cert, tipo_doc, documento, nombres, apellidos, municipio, direccion, email, email_ent, telefono, celular, ocupacion, tipo_doc_ent, documento_ent, razonsocial, municipio_ent, direccion_ent, cargo, unidad_organizacional, organizacion_factel, fecha_cert, formato, vigencia_cert, testigo, foto, pin, pkcs10, soporte, verific_doc, plantilla_huella, token_andesid):
    url_servicio = 'https://ra.andesscd.com.co/test/WebService/soap-server_new.php?wsdl'
    client = Client(url_servicio)
    resultado = client.service.CertificadoFacturacionElectronicaConFechaRequest(tipoCert=tipo_cert, tipoDoc=tipo_doc, documento=documento, nombres=nombres, apellidos=apellidos, municipio=municipio, direccion=direccion, email=email, emailEnt=email_ent, telefono=telefono, celular=celular, ocupacion=ocupacion, tipoDocEnt=tipo_doc_ent, documentoEnt=documento_ent, razonsocial=razonsocial, municipioEnt=municipio_ent, direccionEnt=direccion_ent, cargo=cargo, unidadOrganizacional=unidad_organizacional, organizacionFactel=organizacion_factel, fechaCert=fecha_cert, formato=formato, vigenciaCert=vigencia_cert, testigo=testigo, foto=foto, pin=pin, pkcs10=pkcs10, soporte=soporte, verific_doc=verific_doc, plantillaHuella=plantilla_huella, token_andesid=token_andesid)
    return resultado


def certificado_profesional_titulado(tipo_cert, tipo_doc, documento, nombres, apellidos, municipio, direccion, email, telefono, celular, ocupacion, universidad, tituloprofesional, matriculaprofesional, emisortarjetaprofesional, facultad, fecha_cert, vigencia_cert, formato, testigo, foto, soporte, pin, pkcs10, verific_doc, plantilla_huella):
    url_servicio = 'https://ra.andesscd.com.co/test/WebService/soap-server_new.php?wsdl'
    client = Client(url_servicio)
    resultado = client.service.CertificadoProfesionalTituladoRequest(tipoCert=tipo_cert, tipoDoc=tipo_doc, documento=documento, nombres=nombres, apellidos=apellidos, municipio=municipio, direccion=direccion, email=email, telefono=telefono, celular=celular, ocupacion=ocupacion, universidad=universidad, tituloprofesional=tituloprofesional, matriculaprofesional=matriculaprofesional, emisortarjetaprofesional=emisortarjetaprofesional, facultad=facultad, fechaCert=fecha_cert, vigenciaCert=vigencia_cert, formato=formato, testigo=testigo, foto=foto, soporte=soporte, pin=pin, pkcs10=pkcs10, verific_doc=verific_doc, plantillaHuella=plantilla_huella)
    return resultado


def certificados(tipo_cert, tipo_doc, documento, nombres, apellidos, municipio, direccion, email, telefono, celular, ocupacion, fecha_cert, vigencia_cert, formato, testigo, foto, soporte, pin, pkcs10, verific_doc, plantilla_huella):
    url_servicio = 'https://ra.andesscd.com.co/test/WebService/soap-server_new.php?wsdl'
    client = Client(url_servicio)
    resultado = client.service.CertificadosRequest(tipoCert=tipo_cert, tipoDoc=tipo_doc, documento=documento, nombres=nombres, apellidos=apellidos, municipio=municipio, direccion=direccion, email=email, telefono=telefono, celular=celular, ocupacion=ocupacion, fechaCert=fecha_cert, vigenciaCert=vigencia_cert, formato=formato, testigo=testigo, foto=foto, soporte=soporte, pin=pin, pkcs10=pkcs10, verific_doc=verific_doc, plantillaHuella=plantilla_huella)
    return resultado


def certificados_persona_natural_rut(tipo_cert, tipo_doc, documento, nombres, apellidos, municipio, direccion, email, telefono, celular, ocupacion, fecha_cert, vigencia_cert, formato, testigo, foto, soporte, pin, pkcs10, verific_doc, plantilla_huella):
    url_servicio = 'https://ra.andesscd.com.co/test/WebService/soap-server_new.php?wsdl'
    client = Client(url_servicio)
    resultado = client.service.CertificadosPersonaNaturalRUTRequest(tipoCert=tipo_cert, tipoDoc=tipo_doc, documento=documento, nombres=nombres, apellidos=apellidos, municipio=municipio, direccion=direccion, email=email, telefono=telefono, celular=celular, ocupacion=ocupacion, fechaCert=fecha_cert, vigenciaCert=vigencia_cert, formato=formato, testigo=testigo, foto=foto, soporte=soporte, pin=pin, pkcs10=pkcs10, verific_doc=verific_doc, plantillaHuella=plantilla_huella)
    return resultado

def solicitud_vinculacion_empresa(tipo_cert, tipo_doc, documento, nombres, apellidos, municipio, direccion, email, email_ent, telefono, celular, ocupacion, tipo_doc_ent, documento_ent, razonsocial, municipio_ent, direccion_ent, cargo, unidad_organizacional, fecha_cert, formato, vigencia_cert, testigo, foto, pin, pkcs10, soporte, verific_doc, plantilla_huella, token_andesid):
    url_servicio = 'https://ra.andesscd.com.co/test/WebService/soap-server_new.php?wsdl'
    client = Client(url_servicio)
    resultado = client.service.CertificateVinculacionEmpresaRequest(tipoCert=tipo_cert, tipoDoc=tipo_doc, documento=documento, nombres=nombres, apellidos=apellidos, municipio=municipio, direccion=direccion, email=email, emailEnt=email_ent, telefono=telefono, celular=celular, ocupacion=ocupacion, tipoDocEnt=tipo_doc_ent, documentoEnt=documento_ent, razonsocial=razonsocial, municipioEnt=municipio_ent, direccionEnt=direccion_ent, cargo=cargo, unidadOrganizacional=unidad_organizacional, fechaCert=fecha_cert, formato=formato, vigenciaCert=vigencia_cert, testigo=testigo, foto=foto, pin=pin, pkcs10=pkcs10, soporte=soporte, verific_doc=verific_doc, plantillaHuella=plantilla_huella, token_andesid=token_andesid)
    return resultado




