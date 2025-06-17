    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from .models import Arquivo
from .utils.handleFile import arq_rename, titulo_rename, criarArquivo
import boto3
from botocore.exceptions import ClientError
from django.http import HttpResponse, Http404
from django.conf import settings

class ListarArquivosAPI(APIView):
    def download_arquivo(arquivo):
        s3 = boto3.client(
            's3',
            endpoint_url="http://localhost:9000",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            region_name='us-east-1'
        )

        try:
            response = s3.get_object(Bucket=settings.MINIO_BUCKET_NAME, Key=arquivo.arquivo.name)
            conteudo = response['Body'].read()
        except ClientError:
            raise Http404("Erro ao acessar o arquivo no MinIO.")

        resposta = HttpResponse(conteudo, content_type='application/octet-stream')
        resposta['Content-Disposition'] = f'attachment; filename="{arquivo.titulo}.xlsx"'
        return resposta
    
    def get(self, request):
        """
        Retorna uma lista de arquivos armazenados.
        """
        try:
            arquivos = Arquivo.objects.all().order_by("-data_upload")
            dados = [
                {
                    "id": arq.id_arquivo,
                    "titulo": arq.titulo,
                    "tamanho_MB": arq.tamanho_MB,
                    "data_upload": arq.data_upload,
                    "eliminado": arq.eliminado,
                    "url_download": str(arq.arquivo.url).replace("https", "http") if arq.arquivo else None
                }
                for arq in arquivos
            ]
        except:
            return Response({"erro": "Nenhum arquivo encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(data={"Dados": list((dados))}, status=200)

class InserirArquivoAPI(APIView):
    def post(self, request):
        tabela: list = request.data.get("tabela")
        restricao: list = request.data.get("restricao")
        titulo: str = request.data.get("titulo", "Projeto")
        modo: bool = request.data.get("modo", False)

        if not tabela:
            return Response({"erro": "Conteúdo não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if not titulo:
            return Response({"erro": "Título obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        if Arquivo.objects.filter(titulo=titulo).exists():
            for tr in range(3):
                temp = f"{titulo} ({tr})"
                if Arquivo.objects.filter(titulo=temp).exists() and tr < 3:
                    continue
                elif tr > 3:
                    return Response({"erro": "O título informado já existe. Tente outro título."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    titulo = temp

        arquivoNome = arq_rename(titulo)
        titulo = titulo_rename(titulo)
        file_obj = criarArquivo(tabela, restricao, arquivoNome, modo)
        
        arq = Arquivo.objects.create(
            arquivo=file_obj,
            titulo=titulo,
            tamanho_MB=round(file_obj.size / (1024 * 1024), 2)  # opcional
        )

        return Response({
            "mensagem": "Arquivo enviado com sucesso.",
            "id": arq.id_arquivo,
            "titulo": arq.titulo,
            "tamanho_MB": arq.tamanho_MB,
            "data_upload": arq.data_upload
        }, status=status.HTTP_201_CREATED)

class EliminarArquivoAPI(APIView):
    def post(self, request):
        """
        Elimina um arquivo armazenado.
        """
        id_arquivo = request.data.get("id_arquivo")

        if not id_arquivo:
            return Response({"erro": "ID do arquivo não informado."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            arq = Arquivo.objects.get(id_arquivo=id_arquivo)
            arq.eliminado = True
            arq.save()
        except Arquivo.DoesNotExist:
            return Response({"erro": "Arquivo não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"mensagem": "Arquivo deletado com sucesso."}, status=status.HTTP_200_OK)

class ConsultarArquivoAPI(APIView):
    def get(self, request, *args, **kwargs):
        arquivo_id = kwargs.get('pk')
        try:
            arq = Arquivo.objects.get(id_arquivo=arquivo_id)
        except Arquivo.DoesNotExist:
            return Response({"erro": "Arquivo não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        dados = {
            "id": arq.id_arquivo,
            "titulo": arq.titulo,
            "tamanho_MB": arq.tamanho_MB,
            "data_upload": arq.data_upload,
            "eliminado": arq.eliminado,
            "url_download": arq.arquivo.url,
        }

        try:
            with arq.arquivo.open() as f:
                ctx = pd.read_excel(f)
                dados["contexto"] = ctx.to_dict()  
        except Exception as e:
            dados["contexto"] = f"Erro ao ler arquivo: {str(e)}"

        return Response(dados, status=200)
    
class ImportarArquivo(APIView):
    def post(self, request):
        """
        Importa um arquivo Excel e retorna os dados.

        OBS.: Necessário usar POST para inserir o arquivo no Body.
        """
        arquivo = request.FILES.get("arquivo")

        if not arquivo:
            return Response({"erro": "Arquivo não enviado."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_excel(arquivo)
            dados = df.to_dict(orient="records")
        except Exception as e:
            return Response({"erro": f"Erro ao processar o arquivo: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(dados, status=200)

class ExportarArquivo(APIView):
    def post(self, request):
        """
        Exporta um arquivo Excel com os dados enviados.

        OBS.: Necessário usar POST para inserir o arquivo no Body.
        """
        dados = request.data
        if not dados:
            return Response({"erro": "Dados não enviados."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.DataFrame(dados)   
            buffer = BytesIO()
            df.to_excel(buffer, index=False, )
            buffer.seek(0)
            
            response = HttpResponse(
                buffer,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                status=200
            )
            response['Content-Disposition'] = 'attachment; filename=exportado.xlsx'
            return response
        except Exception as e:
            return Response({"erro": f"Erro ao processar os dados: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
class DownloadArquivoAPI(APIView):
    @staticmethod
    def download_arquivo(arquivo):
        s3 = boto3.client(
            's3',
            endpoint_url="http://localhost:9000",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            region_name='us-east-1'
        )

        try:
            response = s3.get_object(Bucket=settings.MINIO_BUCKET_NAME, Key=arquivo.arquivo.name)
            conteudo = response['Body'].read()
        except ClientError:
            raise Http404("Erro ao acessar o arquivo no MinIO.")

        resposta = HttpResponse(conteudo, content_type='application/octet-stream')
        resposta['Content-Disposition'] = f'attachment; filename="{arquivo.titulo}.xlsx"'
        return resposta

    def get(self, request, *args, **kwargs):
        arquivo_id = kwargs.get('pk')

        try:
            arq = Arquivo.objects.get(id_arquivo=arquivo_id)
        except Arquivo.DoesNotExist:
            return Response({"erro": "Arquivo não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return self.download_arquivo(arq)
