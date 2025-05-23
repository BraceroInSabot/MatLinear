    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .models import Arquivo

class ListarArquivosAPI(APIView):
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
                }
                for arq in arquivos
            ]
        except:
            return Response({"erro": "Nenhum arquivo encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(data={"Dados": list((dados))}, status=200)

class InserirArquivoAPI(APIView):
    def arq_rename(self, arquivo, titulo):
        """
        Renomeia o arquivo.
        """
        ext = arquivo.name.split(".")[-1]
        arquivo.name = f"{titulo}.{ext}"

        return arquivo

    def post(self, request):
        arquivo: object = request.FILES.get("arquivo")
        titulo = request.POST.get("titulo")
        tamanho_MB = round(arquivo.size / (1024 * 1024), 2)

        if not arquivo:
            return Response({"erro": "Arquivo não enviado."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not titulo:
            return Response({"erro": "Título obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if Arquivo.objects.filter(titulo=titulo).exists():
                return Response({"erro": "O título informado já existe. Tente outro título."}, status=status.HTTP_400_BAD_REQUEST)

        arquivo = self.arq_rename(arquivo, titulo)

        arq = Arquivo.objects.create(
            arquivo=arquivo,
            titulo=titulo,
            tamanho_MB=tamanho_MB
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