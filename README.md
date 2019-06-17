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
3. Instale todos os requisitos executando
`python -m pip install -r requirements.txt` no terminal
4. Navegue até a pasta `API` 
5. Execute `python create_settings.py` no terminal para gerar as
configurações necessárias (Caso esteja utilizando PostgreSQL,
configure este antes, e crie uma database a ser usada pela API)

## Instruções
Apenas execute `app.py` no terminal, e a API está pronta
para ser utilizada! 

Os requests são acessíveis pela URL 
mostrada no terminal durante execução do script.

### Para a manipulação de funcionários:

URL/api/v1/funcionarios:
- GET: Retorna todos os funcionários, com filtros opcionais
- POST: Adiciona um funcionário

URL/api/v1/funcionarios/(int:ID):
- GET: Retorna o funcionário específico de id=ID 
- PUT: Atualiza os dados fornecidos do funcionário de id=ID
- DELETE: Deleta o funcionário com id=ID

