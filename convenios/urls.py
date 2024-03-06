from django.contrib import admin
from django.urls import path
from instancias import views
from django.contrib.auth import views as auth_views


from instancias import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.inicio, name='inicio'),
    path('instancias', views.instancia, name='instancia'),
    path('home', views.home, name='home'),
    path('campos_form', views.campos_form, name='campos_form'),
    path('formulario/', views.formulario_instancia, name='formulario'),
    path('cerrar-sesion/', auth_views.LogoutView.as_view(next_page='inicio'), name='cerrar_sesion'),
    path('crear_instancia/', views.crear_instancia, name='crear_instancia'),
    path('obtener_departamentos/', views.obtener_departamentos, name='obtener_departamentos'),
    path('certificado_perso_nat/', views.certificado_perso_nat, name='form-pers-nat'),
    path('certificado_perso_jur/', views.certificado_perso_jur, name='form-pers-jur'),

]
