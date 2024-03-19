from http import client
from django.shortcuts import render, redirect
from suds.client import Client
from django.contrib.auth import authenticate, login
from django.contrib import messages 
from .models import CONVENIO
from django.contrib.auth.hashers import make_password
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import json
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

import requests
from requests import Session

import xml.etree.ElementTree as ET
import base64
from zeep import Client, Transport
from zeep.exceptions import TransportError, XMLSyntaxError

from zeep.wsse.username import UsernameToken


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

def home(request):
    return render (request, 'home.html')



def instancia(request):
    return render (request, 'instancia.html')

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
        logueo = True if request.POST.get('flexRadioDefault1') == 'on' else False
        logo = request.FILES['logo'] if 'logo' in request.FILES else None
        certificados_seleccionados = request.POST.getlist('flexCheckDefault') + request.POST.getlist('flexCheckChecked')
        url = request.POST.get('url')
        color_primario = request.POST.get('colorPrimario')
        color_secundario = request.POST.get('colorSecundario')
        id_vigenica = request.POST.get('id_vigenica')
        banner = True if request.POST.get('flexRadio') == 'on' else False
        contraseña_convenio = request.POST.get('contraseña')
        imagen_banner = request.FILES['imagenBanner'] if 'imagenBanner' in request.FILES else None
        usuario_weservice = request.POST.get('usuario_weservice')
        contraseña_webservice = request.POST.get('contraseña_webservice')
        
        contraseña_convenio_encriptada = make_password(contraseña_convenio)
        print("IDs de los certificados seleccionados:", certificados_seleccionados)
        
        convenio = CONVENIO(
            nombre=nombre,
            logueo=logueo,
            logo=logo,
            certificados_permi=certificados_seleccionados,
            url=url,
            color_primario=color_primario,
            color_secundario=color_secundario,
            id_vigenica=id_vigenica,
            banner=banner,
            imagen_banner=imagen_banner,
            contraseña_convenio=contraseña_convenio_encriptada, 
            usuario_weservice=usuario_weservice,
            contraseña_webservice=contraseña_webservice
        )
        
        convenio.save()
        return redirect('home')
    return render(request, 'home.html')

def formulario_instancia(request):
    return render(request, 'formulario.html')

def campos_form(request):
    departamentos = obtener_departamentos(request)
    print(departamentos)  # Imprimirá los departamentos en la terminal
    return render(request, 'campos-form.html', {'departamentos': departamentos})

def obtener_departamentos(request):
    url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"

    payload = """<soapenv:Envelope xmlns:and="http://www.andesscd.com.co/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
       <soapenv:Header><wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"><wsse:UsernameToken wsu:Id="UsernameToken-7967B371AB1C77594517104219622713"><wsse:Username>PAAN</wsse:Username><wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">WEJdNHmFGnOeCnqNc/vIXRyJafs=</wsse:Password><wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">+fJQ1IEmt2xbAZooSaCNew==</wsse:Nonce><wsu:Created>2024-03-14T13:12:42.268Z</wsu:Created></wsse:UsernameToken></wsse:Security></soapenv:Header>
       <soapenv:Body>
          <and:DepartamentoRequest>
             <and:cadena/>
          </and:DepartamentoRequest>
       </soapenv:Body>
    </soapenv:Envelope>"""

    headers = {
        'Content-Type': 'text/xml',
        'Authorization': 'Basic UEFBTjpnTjlGMnVla3Ru'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        # Parsear la respuesta XML
        root = ET.fromstring(response.content)
        namespaces = {'and': 'http://www.andesscd.com.co/'}
        # Encontrar los elementos que contienen los nombres de los departamentos
        departamentos = root.findall('.//and:Departamento', namespaces)
        nombres_departamentos = [departamento.find('and:nombre', namespaces).text for departamento in departamentos]
        
        # Devolver la lista de nombres de departamentos como respuesta JSON
        return JsonResponse({'departamentos': nombres_departamentos})

    else:
        # Si la solicitud falla, devolver un mensaje de error
        return JsonResponse({'error': 'No se pudo obtener la lista de departamentos'})




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




