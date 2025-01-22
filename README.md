# Automação de Download e Tratamento de Tabelas com Python

Este projeto utiliza o Selenium para realizar a automação do download de arquivos em sites e o pandas para o tratamento de dados em tabelas, além da integração com o BigQuery.
O objetivo é automatizar o processo de coleta, download e manipulação de dados de maneira eficiente.

## 📋 Funcionalidades
- Automação de navegação em sites utilizando o Selenium.
- Download automático de arquivos (por exemplo, planilhas, relatórios, etc.).
- Tratamento e análise de tabelas com a biblioteca pandas.
- Integração com BigQuery para criação de tabelas raw para posterior manipulação dentro do console.

## 🛠️ Tecnologias Utilizadas
- **Python**: Linguagem principal do projeto.
- **Selenium**: Para automação de navegação e downloads.
- **pandas**: Para manipulação e análise de dados.
- **ChromeDriver**: Para controlar o navegador Google Chrome.
- **Google Cloud BigQuery**: Para integração com BigQuery.

## 🚀 Requisitos
Certifique-se de ter as seguintes ferramentas instaladas no seu ambiente:

1. **Python 3.8+**
2. **Google Chrome**
3. **ChromeDriver** (compatível com a versão do Chrome instalada)
4. As dependências listadas no arquivo `requirements.txt`.

## 📦 Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/barbara-sz/BigQuery.git
   cd seu-repositorio
2. Executar arquivo main.py após instalação dos módulos necessários.

## Observações
- Atente-se para alterar os caminhos locais de acordo com a organização do seu computador.
- O chromedriver.exe pode ser adicionado manualmente para que o selenium possa abrir o navegador.
- É necessário ter um arquivo json com os parâmetros relacionados ao projeto para configuração do client, o que possibilita a integração com o BigQuery.
- Apesar de não haver especificação, decidiu-se por utilizar a base completa dos dados que se encontrava em cada arquivo por fazer mais sentido.
- Os cabeçalhos das tabelas foram alterados para seguir o padrão de tabelas SQL, removendo-se acentos, caracteres especiais e espaços.
- Para as tabelas trusted criadas foi aplicado 'SELECT DISTINCT' para que fossem eliminadas linhas duplicadas.
Em geral os dados estavam claros e organizados, não havendo necessidade de maiores edições para esta etapa.
- Para a tabela refinada foi necessária a edição da coluna de data para seguir o padrão ano_mes, baseada no tipo de dado da coluna mes de cada uma das tabelas trusted.
- A variação mensal foi calculada em percentual.
- Foi utilizada a função OVER para ordenar os meses em ordem crescente e a função LAG que se refere ao valor da linha anterior à especificada.
- Conforme regras mandadas por e-mail, foi utilizado JOIN para unir as duas tabelas trusted, o que resultou numa tabela refined somente com meses em que havia ambos os índices.
Para que a nova tabela fosse completa (com todas as datas presentes nos arquivos iniciais) seria necessário utilizar FULL OUTER JOIN.
