from django.urls import path
from .views import (
    ListarArquivosAPI,
    InserirArquivoAPI
)

urlpatterns = [
    path("listar/", ListarArquivosAPI.as_view(), name="listar_arquivos"),
    path("inserir/", InserirArquivoAPI.as_view(), name="inserir_arquivo")
]