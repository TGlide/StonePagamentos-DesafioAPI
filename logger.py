import glob, datetime, os


class Logger():
    """Classe responsável por logar movimentos da manipulação do Banco de Dados da API"""

    def __init__(self):
        # Gerar nome de arquivo
        name = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.log")
        # Criar diretório de logs
        current_path = os.path.dirname(os.path.abspath(__file__))
        logs_path = os.path.join(current_path, "logs/")
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)

        self.file_name = os.path.join(logs_path, name)

    def log(self, request_type, model, *args):
        file_mode = "a"
        if not os.path.isfile(self.file_name):
            file_mode = "w+"  # Cria arquivo caso não exista
            print('f')

        with open(self.file_name, file_mode) as file:
            for s in args:
                if type(s) == str:
                    timestamp = datetime.datetime.now().strftime("[%H:%M:%S] -> ")
                    file.write(timestamp)
                    file.write("{} Request - {}: ".format(request_type, model))
                    file.write(s)
                    file.write("\n")
