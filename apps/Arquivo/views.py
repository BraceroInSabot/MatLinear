    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
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