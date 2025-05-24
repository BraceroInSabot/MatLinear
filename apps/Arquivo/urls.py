from django.urls import path
from .views import (
    ListarArquivosAPI,
    InserirArquivoAPI,
    EliminarArquivoAPI,
    ConsultarArquivoAPI,
    ImportarArquivo,
    ExportarArquivo,
)

urlpatterns = [
    path("listar/", ListarArquivosAPI.as_view(), name="listar_arquivos"),
    path("inserir/", InserirArquivoAPI.as_view(), name="inserir_arquivo"),
    path("eliminar/", EliminarArquivoAPI.as_view(), name="eliminar_arquivo"),
    path("consultar/<int:pk>/", ConsultarArquivoAPI.as_view(), name="consultar_arquivo"),
    path("importar/", ImportarArquivo.as_view(), name="importar_arquivo"),
    path("exportar/", ExportarArquivo.as_view(), name="exportar_arquivo"),
]