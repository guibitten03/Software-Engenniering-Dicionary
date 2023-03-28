# Como rodar o Dicionários:

- No inicio, queria transformar a aplicação em um executável, para rodar em qualquer SO. Mas somente no final do projeto vi que uma aplicação em Dash é muito complexa para transfromar em executável, já que é construida em Flask, que é um framework para desenvolvimento web. 

# Detalhes da implementação:

- A aplicação possui um banco de dados em formato csv própria, para inserção e remoção de definições. Além de possuir uma interface com opções de adicionar, excluir, listar palavras, listar definições e buscar por palavra.

## Como rodar?

Caso 1: Ambiente virtual associado.
1. Navegue até a pasta do projeto pelo terminal.
2. Digite 'source .venv/bin/activate' para entrar no ambiente virtual do python.
3. Digite 'python3 index.py' no terminal. Rodará o programa. Clique com 'ctrl + botão esquerdo do mouse' para abrir na porta localhost.

Caso 2: Ambiente virtual não associado:
- Caso não dê para acessar o ambiente virtual que mandarei no arquivo compilado, é preciso criar um e instalar as depêndencias.
1. Navegue até a pasta do projeto pelo terminal.
2. Digite 'python3 -m venv .venv' no terminal para criar um ambiente virtual.
3. Digite 'source .venv/bin/activate' para entrar no ambiente virtual do python.
4. Digite 'pip3 install -r requirements.txt' para instalar as dependências.
5. Digite 'python3 index.py' no terminal. Rodará o programa. Clique com 'ctrl + botão esquerdo do mouse' para abrir na porta localhost.
