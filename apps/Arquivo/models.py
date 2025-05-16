from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class S3MediaStorage(S3Boto3Storage):
    """
    Armazenamento de arquivos de mídia no MinIO.
    """
    def __init__(self, *args, **kwargs):
        if settings.MINIO_ACCESS_URL:
            self.secure_urls = False
            self.custom_domain = settings.MINIO_ACCESS_URL
        super(S3MediaStorage, self).__init__(*args, **kwargs)

# Descomentar a função para ser armazenado arquivos localmente
#
# def file_upload_to(instance, filename):
#     """
#     Gera um caminho único e seguro para o upload do arquivo.
#     """
#     unique_id = uuid.uuid4().hex
#     sanitized_filename = filename.strip().lower().replace(" ", "_").replace("-", "_")
#     return os.path.join("arquivos", unique_id, sanitized_filename)

class Arquivo(models.Model):
    """
    Modelo representando um arquivo armazenado.
    """
    id_arquivo = models.AutoField(
        primary_key=True,
        verbose_name="ID",
        db_column="ID"
    )
    arquivo = models.FileField(
        storage=S3MediaStorage(),
        verbose_name="Arquivo",
        db_column="Arquivo"
    )
    titulo = models.CharField(
        max_length=255,
        verbose_name="Título",
        db_column="Titulo"
    )
    tamanho_MB = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Tamanho (MB)",
        db_column="TamanhoMB"
    )
    data_upload = models.DateTimeField(
        auto_now_add=True,
        db_column="DataUpload"
    )

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = "Arquivo"
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"
        ordering = ["-data_upload"]

