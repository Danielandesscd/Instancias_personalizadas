from django.shortcuts import render, redirect
from suds.client import Client
from django.contrib.auth import authenticate, login

def inicio(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('contraseña')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Usuario autenticado correctamente, redirigir a una página de inicio.
            return redirect('instancia')
        else:
            # Usuario no autenticado, mostrar un mensaje de error o volver a renderizar el formulario.
            return render(request, 'inicio.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        # Si no es una solicitud POST, simplemente renderiza el formulario de inicio de sesión.
        return render(request, 'inicio.html')


def instancia(request):
    return render (request, 'instancia.html')


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




