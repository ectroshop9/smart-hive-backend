from django.urls import path
from . import views

urlpatterns = [
    path('ingest/', views.ingest, name='vault_ingest'),
    path('verify/', views.verify, name='vault_verify'),
    path('chain/', views.chain, name='vault_chain'),
    path('health/', views.health, name='vault_health'),
]
