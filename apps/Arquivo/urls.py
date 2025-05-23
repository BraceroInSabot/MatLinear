from django.urls import path
from .views import (
    ListarArquivosAPI,
    InserirArquivoAPI,
    EliminarArquivoAPI,
    ConsultarArquivoAPI
)

urlpatterns = [
    path("listar/", ListarArquivosAPI.as_view(), name="listar_arquivos"),
    path("inserir/", InserirArquivoAPI.as_view(), name="inserir_arquivo"),
    path("eliminar/", EliminarArquivoAPI.as_view(), name="eliminar_arquivo"),
    path("consultar/<int:pk>", ConsultarArquivoAPI.as_view(), name="consultar_arquivo"),
]