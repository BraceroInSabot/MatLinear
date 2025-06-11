import tempfile
import os
import re
import pandas as pd
from apps.Arquivo.utils.solver import processar_tabela
from django.core.files import File
from datetime import datetime
from django.core.files.base import ContentFile

def arq_rename(titulo: str) -> str:
    """
    Define o nome do arquivo.

    :param:
        titulo: Título da tabela.
    """
    special = "!@#$%^&*()+=~`{}[]|\\:;\"'<>,.?/"

    if any(char in special for char in titulo):
        titulo = re.sub(r'[^\w\s]', '', titulo)

    titulo = titulo.strip()
    titulo = titulo.lower().replace(" ", "_")

    titulo = f"{titulo}.xlsx"

    return titulo

def titulo_rename(titulo: str) -> str:
    """
    Renomeia o título do arquivo para evitar duplicatas.

    :param:
        titulo: Título do arquivo.
    """
    titulo = titulo.strip()
    titulo = titulo.title()
    return titulo



def criarArquivo(tabela, restricao, arquivoNome: str, modo: bool):
    """
    Cria um arquivo Excel em memória com os dados do solver.
    Retorna um ContentFile pronto para ser salvo no modelo.
    """
    from io import BytesIO

    ctn: dict = processar_tabela(tabela, restricao, modo)
    df_resultado: pd.DataFrame = ctn['Resultado']

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nome_arquivo = f"{arquivoNome}_{timestamp}.xlsx"

    # Cria o Excel em memória
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_resultado.to_excel(writer, sheet_name=arquivoNome, index=False)

    # Cria o ContentFile (lido em memória) com nome
    buffer.seek(0)
    return ContentFile(buffer.read(), name=nome_arquivo)
