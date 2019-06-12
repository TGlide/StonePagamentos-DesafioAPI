# Submissão para Desafio Stone Tecnologia RC
API desenvolvida utilizando Python e Flask, com opção para utilizar 
SQLite ou PostgreSQL como engine para o Banco de Dados

## Requisitos
- Python 3
- Flask
- psycopg2
- Flask-SQLAlchemy

## Instalação
1. Faça o clone do repositório
2. Navegue até o diretório StonePagamentos-DesafioAPI
3. Instale todos os requisitos usando
`pip install -r requirements.txt` 
4. Navegue até a pasta `API` 
5. Execute `create_settings.py` no terminal para gerar as
configurações necessárias (Caso esteja utilizando PostgreSQL,
configure este antes, e crie uma database a ser usada pela API)

## Instruções
Apenas execute `app.py` no terminal, e a API está pronta
para ser utilizada! 

Por padrão, os requests são acessíveis
por http://localhost:5000/, e por 
http://localhost:5000/api/v1/funcionarios para a manipulação
de funcionários.

