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
    

def listar_convenios(request):
    convenios = CONVENIO.objects.all()
    print(convenios)

    return render(request, 'home.html', {'convenios': convenios})


def detalle_convenio(request, convenio_id):
    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    return render(request, 'plantilla_convenio.html', {'convenio': convenio})




def home(request):
    return render (request, 'home.html')

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



def crear_instancia(request):
    if request.method == 'POST':
        
        nombre = request.POST.get('nombre')
        logueo = True if request.POST.get('flexRadioDefault1') == 'on' else False
        logo = request.FILES['logo'] if 'logo' in request.FILES else None
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

        
        convenio = CONVENIO(
            nombre=nombre,
            logueo=logueo,
            logo=logo,
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



def obtener_departamentos(request):
    # Configurar las credenciales de autenticación
    username = 'PAAN'
    password = 'gN9F2uektn'

    # Crear un cliente SOAP con el URL del servicio y las credenciales
    client = Client('https://ra.andesscd.com.co/test/WebService/soap-server_new.php', wsse=UsernameToken(username, password))

    # Hacer la solicitud SOAP
    response = client.service.DepartamentoRequest(cadena='')

    # Extraer los departamentos de la respuesta SOAP
    departamentos = response.lista_departamentos

    return render(request, 'campos-form.html', {'departamentos': departamentos})





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




