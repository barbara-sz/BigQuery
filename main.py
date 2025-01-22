from funcoes import download_tabela, tratar_tabela, carregar_tabela, renomear_arquivo
from google.cloud import bigquery


# links para download das tabelas
link_icc = 'https://www.fecomercio.com.br/pesquisas/indice/icc'
link_icf = 'https://www.fecomercio.com.br/pesquisas/indice/icf'

caminho = r'/app/Downloads'

# configuração do cliente BigQuery
client = bigquery.Client.from_service_account_json(r'/app/SA-b_szortika.json')

# parâmetros do projeto e dataset
project_id = 'ps-eng-dados-ds3x'
dataset_id = 'ps-eng-dados-ds3x.b_szortika'

if __name__ == '__main__':

    # fazendo download das tabelas
    download_tabela(link_icc)
    download_tabela(link_icf)

    # renomeando arquivos
    renomear_arquivo('icc.xlsx', caminho)
    renomear_arquivo('icf.xlsx', caminho)

    # tratando tabelas
    icc_df = tratar_tabela(caminho+"/"+"icc.xlsx", 'SÉRIE')
    icf_df = tratar_tabela(caminho+"/"+"icf.xlsx", 'Série Histórica')

    # carregando tabelas no BigQuery
    carregar_tabela(icc_df, "icc_raw", dataset_id, client)
    carregar_tabela(icf_df, "icf_raw", dataset_id, client)
