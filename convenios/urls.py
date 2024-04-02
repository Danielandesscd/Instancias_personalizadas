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
    path('obtener_municipios_ajax/', views.obtener_municipios_ajax, name='obtener_municipios_ajax'),
    path('instancias', views.instancia, name='instancia'),
    path('home', views.home, name='home'),
    path('campos_form', views.campos_form, name='campos_form'),
    path('formulario/', views.formulario_instancia, name='formulario'),
    path('cerrar-sesion/', auth_views.LogoutView.as_view(next_page='inicio'), name='cerrar_sesion'),
    path('crear_instancia/', views.crear_instancia, name='crear_instancia'),
    path('guardar_convenios/', views.guardar_convenios, name='guardar_convenios'),
    path('obtener_departamentos/', views.obtener_departamentos, name='obtener_departamentos'),
    path('certificado_perso_nat/', views.certificado_perso_nat, name='form-pers-nat'),
    path('certificado_perso_jur/', views.certificado_perso_jur, name='form-pers-jur'),
    path('certificado_perso_nat_rut/', views.certificado_perso_nat_rut, name='form-pers-nat-rut'),
    path('certificado_pert_emp/', views.certificado_pert_emp, name='form-pert-emp'), 
    path('certificado_prof_titu/', views.certificado_prof_titu, name='form-prof-titu'),
    path('certificado_fact_pj/', views.certificado_fact_pj, name='form-fe-pj'),
    path('certificado_fact_pn/', views.certificado_fact_pn, name='form-fe-pn'),
    path('consultar/', views.consultar, name='consultar'),
    path('revocar/', views.revocar, name='revocar'),
    path('cambiar_pin/', views.cambiar_pin, name='cambiar_pin'),
    path('firmar_doc/', views.firmar_doc, name='firmar_doc'),
    path('instancia/<str:nombre_empresa>/', views.instancia_empresa, name='instancia'),
    path('plantilla_dinamica/<int:convenio_id>/', views.plantilla_dinamica, name='detalle_convenio'),
    path('plantilla_convenio/<int:id>/', views.plantilla_convenio, name='plantilla_convenio'),
    path('login_instancia/', views.login_instancia, name='login_instancia'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
