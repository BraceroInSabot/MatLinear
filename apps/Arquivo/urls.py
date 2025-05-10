from django.urls import path
from .views import (
    ListarArquivosAPI
)

urlpatterns = [
    path("listar/", ListarArquivosAPI.as_view(), name="listar_arquivos"),
]