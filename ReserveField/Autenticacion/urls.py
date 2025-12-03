from django.urls import path
from . import views

urlpatterns = [
    path('', views.Autentificacion, name='autenticacion'),
    path('logout/', views.logout_view, name='logout'),
]
