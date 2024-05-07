from django.contrib import admin
from django.urls import path
from instancias import views
from django.contrib.auth import views as auth_views
from instancias import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.inicio, name='inicio'),
    path('obtener_departamentos/', views.obtener_departamentos, name='obtener_departamentos'),
    path('obtener_municipios/<int:departamento_id>/', views.obtener_municipios, name='obtener_municipios'),
    path('instancias', views.instancia, name='instancia'),
    path('home', views.home, name='home'),
    path('campos_form', views.campos_form, name='campos_form'),
    path('formulario/', views.formulario_instancia, name='formulario'),
    path('cerrar-sesion/', auth_views.LogoutView.as_view(next_page='inicio'), name='cerrar_sesion'),
    path('crear_instancia/', views.crear_instancia, name='crear_instancia'),
    #path('guardar_convenios/', views.guardar_convenios, name='guardar_convenios'),
    path('form_pers_nat/', views.form_pers_nat, name='form_pers_nat'),
    path('form_pers_jur/', views.form_pers_jur, name='form_pers_jur'),
    path('form_pers_nat_rut/', views.form_pers_nat_rut, name='form_pers_nat_rut'),
    path('form_pert_emp/', views.form_pert_emp, name='form_pert_emp'), 
    path('form_prof_titu/', views.form_prof_titu, name='form_prof_titu'),
    path('form_fe_pj/', views.form_fe_pj, name='form_fe_pj'),
    path('form_fe_pn/', views.form_fe_pn, name='form_fe_pn'),
    path('consultar/', views.consultar, name='consultar'),
    path('revocar/', views.revocar, name='revocar'),
    path('cambiar_pin/', views.cambiar_pin, name='cambiar_pin'),
    path('firmar_doc/', views.firmar_doc, name='firmar_doc'),
    path('instancia/<str:nombre_empresa>/', views.instancia_empresa, name='instancia'),
    path('plantilla_dinamica/<int:convenio_id>/', views.plantilla_dinamica, name='detalle_convenio'),
    path('plantilla_convenio/<int:id>/', views.plantilla_convenio, name='plantilla_convenio'),
    path('login_instancia/<int:convenio_id>/', views.login_instancia, name='login_instancia'),
    path('formulario_certificado/<int:id_convenio>/', views.formulario_certificado, name='formulario_certificado'),
    path('guardar_certificado/', views.guardar_certificado, name='guardar_certificado'),
    path('formulario1/', views.formulario1, name='formulario1'),
    path('procesar-formulario/', views.procesar_formulario, name='procesar_formulario'),
    path('verificar_convenio/<int:convenio_id>/', views.verificar_convenio, name='verificar_convenio'),
    path('login_instancia/', views.login_instancia, name='login_instancia'),
    path('credenciales_webservice/', views.credenciales_webservice, name='credenciales_webservice'),
    path('generar_cabecera_soap/', views.generar_cabecera_soap, name='generar_cabecera_soap'),
    path('radicado_pers_nat/', views.radicado_pers_nat, name='radicado_pers_nat'),
    path('radicado_pers_nat_rut/', views.radicado_pers_nat_rut, name='radicado_pers_nat_rut'),
    path('obtener_universidades/<int:municipio_id>/', views.obtener_universidades, name='obtener_universidades'),
    path('radicado_prof_titulado/', views.radicado_prof_titulado, name='radicado_prof_titulado'),
    path('obtener_titulos/<int:universidad_id>/', views.obtener_titulos, name='obtener_titulos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)