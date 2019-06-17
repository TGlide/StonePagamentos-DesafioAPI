import os
import time
from configparser import ConfigParser
from .helpers import clear_screen, screen_prompt

if __name__ == "__main__":
    os.system(clear_screen())
    print("#################################")
    print("BEM-VINDO AO SETUP INICIAL DA API")
    print("#################################")

    current_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_path, "settings.ini")
    config = ConfigParser()
    config['database'] = {}

    time.sleep(2)
    os.system(clear_screen())

    # Escolha de engine
    db_options = {
        "1": "SQLite",
        "2": "PostgreSQL"
    }
    config['database']['engine'] = screen_prompt("Qual engine você deseja usar?", db_options)
    os.system(clear_screen())
    config['database']['db_name'] = input("Qual o nome da database?")

    # Escolha de port, host, e nome (caso seja Postgres)
    if config['database']['engine'] == "PostgreSQL":
        os.system(clear_screen())
        config['database']['host'] = input("Qual o host? (Deixe em branco para localhost)")
        if config['database']['host'] == '':
            config['database']['host'] = "localhost"

        os.system(clear_screen())
        config['database']['port'] = input("Qual o port? (Deixe em branco para 5432)")
        if config['database']['port'] == '':
            config['database']['port'] = "5432"

        # Informações de login
        os.system(clear_screen())
        config['database']['user'] = input("Qual o username?")

        os.system(clear_screen())
        config['database']['pw'] = input("Qual a senha de {}?".format(config['database']['user']))

    with open(config_path, "w") as f:
        config.write(f)

    os.system(clear_screen())
    print("Configurações criadas!")

    try:
        from API.app import db
        db.create_all()
    except Exception as e:
        print("Erro ao criar database, por favor execute novamente o script de configuração.({})".format(e))
    else:
        print("Database criada com sucesso!")

    time.sleep(1)
