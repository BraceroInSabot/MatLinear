    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Arquivo

class ListarArquivosAPI(APIView):
    def get(self, request):
        return Response("Oi", status=200)

class InserirArquivoAPI(APIView):
    def post(self, request):
        arquivo = request.FILES.get("arquivo")
        titulo = request.POST.get("titulo")
        tamanho_MB = request.POST.get("tamanho_MB")

        if not arquivo:
            return Response({"erro": "Arquivo não enviado."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not titulo or not tamanho_MB:
            return Response({"erro": "Título e tamanho são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)


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

   