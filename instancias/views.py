from http import client
from django.shortcuts import render, redirect
import psycopg2
from suds.client import Client
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CONFI_CERTIFICADOS, CONVENIO, TIPO_CERT
from django.contrib.auth.hashers import make_password
from zeep import Client
import base64
import hashlib
import datetime
import random
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import json
from django.conf import settings
from django.template.loader import render_to_string
import os
from django.template import TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
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
from django.shortcuts import render, get_object_or_404
import hashlib
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
    

def login_instancia(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        try:
            convenio = CONVENIO.objects.get(usuario=usuario, contraseña=contraseña)
            return redirect('plantilla_convenio')
        except CONVENIO.DoesNotExist:
             return render(request, 'login_instancia.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'login_instancia.html')
    
    
def plantilla_convenio(request, id):
    convenio = get_object_or_404(CONVENIO, id=id)
    return render(request, 'plantilla_convenio.html', {'convenio': convenio})
    

def detalle_convenio(request, convenio_id):
    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    return render(request, 'plantilla_convenio.html', {'convenio': convenio})



def home(request):
    convenios = CONVENIO.objects.all()
    return render(request, 'home.html', {'convenios': convenios})





def plantilla_dinamica(request, convenio_id):
    mapeo_tipos_certificado = {
    "10": "Facturación Electrónica - Persona Jurídica",
    "11": "Facturación Electrónica - Persona Natural",
    "6": "Comunidad Académica",
    "9": "Pertenencia Empresa",
    "7": "Profesional Titulado",
    "8": "Representante Legal",
    "12": "Función Pública",
    "13": "Persona Jurídica",
    "14": "Función Pública para SIIF Nación",
    "5": "Persona Natural",
    "15": "Persona Natural Para Actividad Comercial(Rut)"
}
    
    mapeo_certificados_formularios = {
        "10": 'form_fe_pj',
        "11": 'form_fe_pn',
        #"6": 'form-com-acad.html',
        "9": 'form_pert_emp',
        "7": 'form_prof_titu',
        #"8": 'form-rep-legal.html',
        #"12": 'form-func-pub.html',
        "13": 'form_pers_jur',
        #"14": 'form-func-pub-nacion.html',
        "5": 'form_pers_nat',
        "15": 'form_pers_nat_rut'
    }

    

    mapeo_operacion_cert = {
        "1" : 'consultar',
        "2" : 'revocar',
        "3" : 'cambiar_pin',
        "4" : 'reposicion'

    }

    mapeo_operaciones_firmado = {
        "1" : 'firmar_doc',
        "2" : 'verificar_firma'
    }

    mapeo_operaciones_otp = {
        "1" : 'cambiar_tiempo',
        "2" : 'firmar_otp',
        "3" : 'invalidar'

    }





    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    confi_certificados = CONFI_CERTIFICADOS.objects.filter(id_convenio=convenio.id)

    certificados_con_nombre_y_formulario = [
        {
            'tipo_certificado': mapeo_tipos_certificado.get(str(cert.tipo_certificado), 'Tipo desconocido'),
            'formulario': mapeo_certificados_formularios.get(str(cert.tipo_certificado), '#'),  # Default to '#'
            'detalles_certificado': cert,
        }
        for cert in confi_certificados
    ]

    for cert in confi_certificados:
       
        print("Tipo de Certificado:", cert.tipo_certificado) 
          
        print("---")
    
    print("color: ", convenio.color_primario)
    print("Nombre del convenio:", convenio.nombre)
    print("Color primario del convenio:", convenio.color_primario)
    
   

    
    numeros_operacion_cert = convenio.o_cert_permi.split(',') if convenio.o_cert_permi else []
    operaciones_certificado = [mapeo_operacion_cert.get(numero) for numero in numeros_operacion_cert]

    
    numeros_operaciones_firmado = convenio.o_firmado_permi.split(',') if convenio.o_firmado_permi else []
    operaciones_firmado = [mapeo_operaciones_firmado.get(numero) for numero in numeros_operaciones_firmado]

    
    numeros_operaciones_otp = convenio.o_otp_permi.split(',') if convenio.o_otp_permi else []
    operaciones_otp = [mapeo_operaciones_otp.get(numero) for numero in numeros_operaciones_otp]

    return render(request, 'plantilla_convenio.html', {
        'convenio': convenio,
        'certificados_con_nombre_y_formulario': certificados_con_nombre_y_formulario,
        'operaciones_certificado': operaciones_certificado,
        'operaciones_firmado': operaciones_firmado,
        'operaciones_otp': operaciones_otp
    
    })



def formulario_dinamico(request, convenio_id):
    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    print("Nombre del convenio for:", convenio.nombre)
    print("Color primario del convenio for:", convenio.color_primario)
    #return render(request, 'form-pers-nat.html', {'convenio': convenio})
    return render(request, 'form-pers-nat.html', {
        'convenio_id': convenio.id,
        'convenio_nombre': convenio.nombre,
    })


def verificar_convenio(request, convenio_id):
    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    if convenio.contraseña_convenio:
        return redirect('login_instancia', convenio_id=convenio_id)
    else:
        return render(request, 'plantilla_convenio.html', {'convenio': convenio})

def login_instancia(request, convenio_id):
    convenio = get_object_or_404(CONVENIO, pk=convenio_id)
    if request.method == 'POST':
        contraseña = request.POST.get('contraseña')
        convenio_valido = CONVENIO.objects.filter(pk=convenio_id, contraseña_webservice=contraseña).first()
        if convenio_valido:
            return redirect('plantilla_convenio', id=convenio_id) 
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login_instancia.html', {'convenio': convenio})





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

def form_pers_nat(request):
    return render (request, 'form_pers_nat.html')

def form_pers_jur(request):
    return render (request, 'form_pers_jur.html')

def form_pers_nat_rut(request):
    return render (request, 'form_per_nat_rut.html')

def form_pert_emp(request):
    return render (request, 'form_pert_emp.html')

def form_prof_titu(request):
    return render (request, 'form_prof_titu.html')

def form_fe_pj(request):
    return render (request, 'form_fe_pj.html')

def form_fe_pn(request):
    return render (request, 'form_fe_pn.html')


def procesar_formulario_convenio(request):
    if request.method == 'POST':
        convenio = CONVENIO(nombre=request.POST['nombre'])
        convenio.save()
        
        certificados_seleccionados_ids = request.POST.getlist('tipos_certificados')
        
        for certificado_id in certificados_seleccionados_ids:
            TIPO_CERT = TIPO_CERT.objects.get(pk=certificado_id)
            convenio.certificados_seleccionados.add(TIPO_CERT)
        
        return render(request, 'tu_template.html', {'convenio': convenio})
    else:
        return render(request, 'tu_formulario.html')



# @csrf_exempt
# def guardar_convenios(request):
#     if request.method == 'POST':
#         data = request.POST.dict()

#         certificados_seleccionados = [key for key, value in data.items() if value == 'on']

#         tipo_certificado = ','.join(certificados_seleccionados)

#         convenio = CONFI_CERTIFICADOS(tipo_certificado=tipo_certificado)
#         convenio.save()

#         return JsonResponse({'message': 'Convenios guardados correctamente.'})

#     return JsonResponse({'error': 'Se esperaba una solicitud POST.'}, status=400)

def instancia_empresa(request, nombre_empresa):
    template_name = f'instancia_empresas/{nombre_empresa}.html'
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        return HttpResponseServerError(f'Error: La plantilla "{template_name}" no existe.')

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

        consultar_certificado = request.POST.get('consultar_certificado')
        revocar_certificado = request.POST.get('revocar_certificado')
        cambiar_pin = request.POST.get('cambiar_pin')
        reposicion_certificado = request.POST.get('reposicion_certificado')
        
        firmar_documento = request.POST.get('firmar_documento')
        verificar_firma = request.POST.get('verificar_firma')
        
        cambiar_otp = request.POST.get('cambiar_otp')
        firmar_con_otp = request.POST.get('firmar_con_otp')
        invalidar_otp = request.POST.get('invalidar_otp')
        
        vigencia_1_dia = request.POST.get('vigencia_1_dia')
        vigencia_1_mes = request.POST.get('vigencia_1_mes')
        vigencia_3_meses = request.POST.get('vigencia_3_meses')
        vigencia_6_meses = request.POST.get('vigencia_6_meses')
        vigencia_1_ano = request.POST.get('vigencia_1_ano')
        vigencia_18_meses = request.POST.get('vigencia_18_meses')
        vigencia_2_anos = request.POST.get('vigencia_2_anos')
        
        token_virtual = request.POST.get('token_virtual')
        token_fisico = request.POST.get('token_fisico')
        pkcs10 = request.POST.get('pkcs10')



        certificados_permi = ','.join(filter(None, [ certificado_Representante_Legal,certificado_Funcion_Publica ,certificado_Funcion_Publica,certificado_Facturacion_Electronica_Persona_JurÍdica,certificado_Facturacion_Electronica_Persona_Natural,certificado_Persona_Natural_Con_RUT,certificado_Profesional_Titulado ,certificado_Función_Publica_SIIF_Nación,certificado_Comunidada_Académica,certificado_persona_natural, certificado_persona_juridica, certificado_pertenencia_empresa]))
        print("Certificados permiso:", certificados_permi)   #Imprimir en la terminal
        o_cert_permi = ','.join(filter(None, [consultar_certificado, revocar_certificado, cambiar_pin, reposicion_certificado]))
        
        o_firmado_permi = ','.join(filter(None, [firmar_documento, verificar_firma]))
        
        o_otp_permi = ','.join(filter(None, [cambiar_otp, firmar_con_otp, invalidar_otp]))
        
        vigencias_permi = ','.join(filter(None, [vigencia_1_dia, vigencia_1_mes, vigencia_3_meses, vigencia_6_meses, vigencia_1_ano, vigencia_18_meses, vigencia_2_anos]))
        
        formatos_entrega_permi = ','.join(filter(None, [token_virtual, token_fisico, pkcs10]))


        user = User.objects.create_user(username=usuario_weservice, password=contraseña_webservice)


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
            id_user = user
        )

        

        convenio.usuario = user
        convenio.save()
        # Después de guardar los datos, obtenemos el id del convenio creado
        id_convenio = convenio.id

        # Redirigimos al usuario a formulario_certificado.html y pasamos el id del convenio como parte del contexto
        return redirect('formulario_certificado', id_convenio=id_convenio)

    return render(request, 'home.html')

def formulario_certificado(request, id_convenio):
    convenio = get_object_or_404(CONVENIO, id=id_convenio)  # Verificamos que el id es válido
    return render(request, 'formulario_certificado.html', {'convenio': convenio})

@csrf_exempt  # Esto permite solicitudes POST sin protección CSRF (útil para pruebas pero cuidado en producción)
def guardar_certificado(request):
    if request.method == "POST":
        try:
            # Obtener datos del cuerpo del POST
            data = json.loads(request.body)
            print("Datos recibidos en el servidor:", data)

            # Validar campos críticos
            id_convenio = data.get("id_convenio")
            tipo_certificado = data.get("tipoCertificado", "")
            vigencias = data.get("vigencias", [])  # Convertir a lista de enteros
            formatos = data.get("formatos", [])  # Convertir a lista de cadenas

            # Validar existencia de id_convenio
            if not id_convenio:
                return JsonResponse({"error": "Falta id_convenio"}, status=400)

            # Verificar que vigencias y formatos no estén vacíos
            if not formatos:
                return JsonResponse({"error": "Falta 'formatos'."}, status=400)
            if not vigencias:
                return JsonResponse({"error": "Falta 'vigencias'."}, status=400)

            # Obtener el convenio
            convenio = CONVENIO.objects.get(id=id_convenio)

            # Crear el nuevo certificado
            nuevo_certificado = CONFI_CERTIFICADOS(
                id_convenio=convenio,
                tipo_certificado=tipo_certificado,
                vigencias=vigencias,  # Asegúrate de que sea lista de enteros
                formatos=formatos  # Establece la lista correctamente
            )

            # Guardar el certificado
            nuevo_certificado.save()

            return JsonResponse({"message": "Datos guardados correctamente"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos mal formateados"}, status=400)
        except CONVENIO.DoesNotExist:
            return JsonResponse({"error": "El convenio no existe"}, status=404)
        except Exception as e:
            print("Error inesperado:", str(e))
            return JsonResponse({"error": "Error inesperado al procesar la solicitud"}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)


def formulario_instancia(request):
    return render(request, 'formulario.html')

def formulario1(request):
    departamentos = obtener_departamentos()  # Llamar a la función para obtener la lista de departamentos
    return render(request, 'formulario1.html', {'departamentos': departamentos})
def procesar_formulario(request):
    if request.method == 'POST':
        # Aquí puedes procesar los datos del formulario enviado
        # Por ejemplo, puedes acceder a los datos del formulario usando request.POST
        
        # Luego, puedes realizar cualquier lógica de procesamiento necesaria
        # Por ahora, simplemente devolveremos una respuesta de éxito
        return HttpResponse('¡Formulario procesado con éxito!')
    else:
        # Si la solicitud no es POST, puedes manejarlo según sea necesario
        return HttpResponse('¡Solicitud no válida!')
def campos_form(request):
    departamentos = obtener_departamentos()
    print("departamentos:", departamentos)  # Imprimirá los departamentos en la terminal
    return render(request, 'campos-form.html', {'departamentos': departamentos})


def obtener_conexion_db():
    return psycopg2.connect(
        dbname=settings.DATABASES["default"]["NAME"],
        user=settings.DATABASES["default"]["USER"],
        password=settings.DATABASES["default"]["PASSWORD"],
        host=settings.DATABASES["default"]["HOST"],
        port=settings.DATABASES["default"]["PORT"],
    )


@login_required
def credenciales_webservice(request):
    if request.method == "POST":
        user = request.user
        
        try:
            convenios = user.CONVENIO.all()
            
            if convenios.exists():
                convenio = convenios.first()  # Obtener el primer convenio
                usuario_webservice = convenio.usuario_weservice
                contrasena_webservice = convenio.contraseña_webservice

                print("Usuario Webservice antes de llamar a crear_cabecera_soap:", usuario_webservice)
                print("Contraseña Webservice antes de llamar a crear_cabecera_soap:", contrasena_webservice)
                cabecera_soap = crear_cabecera_soap("TestUser", "TestPassword")
                print("Cabecera SOAP:", cabecera_soap)

                return JsonResponse({'status': 'success'})

            else:
                return JsonResponse({'status': 'error', 'message': 'No se encontró ningún convenio para este usuario'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return redirect('home')


def crear_cabecera_soap(username, password):
    # Generar 'created'
    tm_created = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Generar 'nonce'
    simple_nonce = random.randint(0, 1000000)
    encoded_nonce = base64.b64encode(str(simple_nonce).encode()).decode()

    # Calcular 'password digest'
    passdigest = base64.b64encode(
        hashlib.sha1(f"{simple_nonce}{tm_created}{password}".encode()).digest()
    ).decode()

    # Crear la cabecera SOAP
    cabecera = f"""
    <soapenv:Header>
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
            <wsse:UsernameToken wsu:Id="UsernameToken-7967B371AB1C77594517104219622713">
                <wsse:Username>{username}</wsse:Username>
                <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{passdigest}</wsse:Password>
                <wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{encoded_nonce}</wsse:Nonce>
                <wsu:Created>{tm_created}</wsu:Created>
            </wsse:UsernameToken>
        </wsse:Security>
    </soapenv:Header>
    """
    
    return cabecera

def obtener_departamentos():
    url = "https://ra.andesscd.com.co/test/WebService/soap-server_new.php"
    # Crea la cabecera SOAP
    cabecera = crear_cabecera_soap()

    body = """
    <soapenv:Body>
        <and:DepartamentoRequest>
            <and:cadena/>
        </and:DepartamentoRequest>
    </soapenv:Body>
    """
    payload = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:and="http://www.andesscd.com.co/">
        {cabecera}
        {body}
    </soapenv:Envelope>
    """
    headers = {
      'Content-Type': 'text/xml'
    }

    try:
        # Realiza la solicitud SOAP
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status() 
        
      
        root = ET.fromstring(response.content)
        mensaje = root.find(".//{http://www.andesscd.com.co/}mensaje").text
        departamentos = json.loads(mensaje)
        
        return departamentos
    
    except requests.exceptions.RequestException as e:
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
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Lanza una excepción si la solicitud falla (por ejemplo, código de estado HTTP diferente de 200)
        
        root = ET.fromstring(response.content)
        municipios = []
        print("municipios:",root)
        print("print:",response)

        for municipio in root.findall('.//and:Municipio', namespaces={'and': 'http://www.andesscd.com.co/'}):
            id_municipio = municipio.find('.//and:id_municipio', namespaces={'and': 'http://www.andesscd.com.co/'}).text
            nombre = municipio.find('.//and:nombre', namespaces={'and': 'http://www.andesscd.com.co/'}).text
            municipios.append({'id': id_municipio, 'nombre': nombre})
        
        return municipios
    
    except requests.exceptions.RequestException as e:
        
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