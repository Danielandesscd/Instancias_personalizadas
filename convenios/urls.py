from django.contrib import admin
from django.urls import path
from instancias import views

from instancias import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.inicio, name='inicio'),

    path('instancias', views.instancia, name='instancia'),
    path('home', views.home, name='home'),

]
