from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import time
import glob
import os
import pandas as pd


# função para entrar no site, fazer download da tabela
def download_tabela(link):
    navegador = webdriver.Chrome()  # abrindo google chrome
    navegador.get(link)  # entrando na página para efetuar o download da tabela icc

    # aguardar aparecer o botão enquanto a página carrega
    element = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'download')))

    element.click()  # faz download

    time.sleep(2)


# função para renomear arquivo
def renomear_arquivo(novo_nome, caminho):

    termo = novo_nome.replace('.xlsx', '')
    # Procurar arquivos na pasta que contenham o termo
    arquivos = glob.glob(os.path.join(caminho, f"*{termo}*"))

    if not arquivos:
        return f"Nenhum arquivo encontrado contendo o termo '{termo}' na pasta '{caminho}'"

    # Encontrar o arquivo mais recente com base na data de modificação
    arquivo_mais_recente = max(arquivos, key=os.path.getmtime)

    # Caminho completo do novo nome
    caminho_novo_nome = os.path.join(caminho, novo_nome)

    # Renomear o arquivo
    os.rename(arquivo_mais_recente, caminho_novo_nome)

    return f"Arquivo '{arquivo_mais_recente}' foi renomeado para '{caminho_novo_nome}'"


# função para carregar tabelas, reestruturar colunas e adicionar a coluna load_timestamp
def tratar_tabela(caminho, aba):
    df = pd.read_excel(caminho, sheet_name=aba)

    # verifica se há colunas "Unnamed"
    if any("Unnamed" in str(col) for col in df.columns):
        df.columns = df.iloc[0]  # define a primeira linha como cabeçalho
        df = df[1:].reset_index(drop=True)  # remove a linha usada como cabeçalho e redefine os índices

    # função para normalizar as colunas, seguindo o padrão do banco de dados
    def normalizar_coluna(coluna):
        # remover espaços antes e depois
        coluna = coluna.strip()
        # remover acentos
        coluna = ''.join(
            char for char in unicodedata.normalize('NFD', coluna)
            if unicodedata.category(char) != 'Mn'
        )
        # substituir "+" por "mais"
        coluna = coluna.replace('+', 'mais')
        # substituir espaços por "_"
        coluna = coluna.replace(' ', '_')
        # converter para minúsculas
        coluna = coluna.lower()
        return coluna

    df.columns = list(map(normalizar_coluna, df.columns))
    df['load_timestamp'] = datetime.utcnow()

    return df


# função para carregar dados no BigQuery
def carregar_tabela(df, table_id, dataset_id, client):
    try:
        client.get_dataset(dataset_id)  # tenta obter o dataset
        print(f"Dataset '{dataset_id}' já existe.")

    except NotFound:
        # se o dataset não existir, criar
        print(f"Dataset '{dataset_id}' não encontrado. Criando o dataset...")
        dataset = bigquery.Dataset(dataset_id)
        client.create_dataset(dataset)  # cria o dataset
        print(f"Dataset '{dataset_id}' criado com sucesso.")

    table_full_id = f"{dataset_id}.{table_id}"

    job = client.load_table_from_dataframe(df, table_full_id)  # carrega a tabela
    job.result()  # aguarda o job ser concluído
    print(f"Tabela {table_id} carregada com sucesso.")
