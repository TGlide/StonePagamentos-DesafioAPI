import os

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from API.logger import Logger

############################################
# Configurações do app e do Banco de Dados #
############################################
app = Flask(__name__)  # Inicializa app

# Abre configurações
current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, "settings.ini")
config = ConfigParser()
config.read(config_path)
db_config = config['database']

# Escolhe a database baseada nas configurações
if config['database']['engine'] == "SQLite":
    db_path = os.path.join(current_path, '{}.db'.format(db_config['db_name']))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}'.format(db_path)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(db_config['user'],
                                                                                      db_config['pw'],
                                                                                      db_config['host'],
                                                                                      db_config['port'],
                                                                                      db_config['db_name'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Inicializa Banco de Dados

logger = Logger()  # Inicializa Logger


###########
# Modelos #
###########
class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    cargo = db.Column(db.String(128), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    attributos = ['nome', 'cargo', 'idade']

    def __repr__(self):
        return '<Funcionário %r>' % self.nome

    def serialize(self):
        """Retorna a instância de Funcionário em formato serializável"""
        serialized = {a: getattr(self, a) for a in self.attributos}
        serialized['id'] = self.id
        return serialized


#########
# Rotas #
#########
@app.route('/', methods=['GET'])
def home():
    return '<h1>Bem-vindo a API desafiadora da Stone Pagamentos!</h1>' \
           '<p>Thomas G. Lopes</p>'


@app.route('/api/v1/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    """Manipula as entradas de funcionários no banco de dados"""

    if request.method == 'GET':
        # Aplica filtros
        nome = request.args.get('nome', default='')
        idade = request.args.get('idade')
        cargo = request.args.get('cargo', default='')
        func = Funcionario.query.filter(Funcionario.nome.contains(nome), Funcionario.cargo.contains(cargo))
        if idade:
            func = func.filter_by(idade=idade)

        # Cria lista de todos os funcionários em formato serializável
        func_lista = [f.serialize() for f in func]

        logger.log("GET", "Funcionario", "{} iten(s) foram retornados (Sem filtros)".format(len(func_lista)))
        return jsonify(func_lista)

    elif request.method == 'POST':
        # Erro: Post efetuado sem dados
        if not request.form:
            logger.log("POST", "Funcionario", "Erro: POST sem form-data")
            abort(400)

        # Cria funcionario
        f = Funcionario()
        try:
            f.nome = request.form['nome']
            f.idade = int(request.form['idade'])
            f.cargo = request.form['cargo']
        # Erro: POST efetuado sem todos os dados necessários
        except Exception as e:
            logger.log("POST", "Funcionario", "Erro: POST com form-data incompleto")
            abort(400)
        else:
            # Adiciona funcionário ao DB
            db.session.add(f)
            db.session.commit()
            logger.log("POST", "Funcionario", "Add Funcionário {}".format(f))
            return jsonify(f.serialize())


@app.route('/api/v1/funcionarios/<int:identifier>', methods=['GET', 'PUT', 'DELETE'])
def funcionarios_id(identifier):
    """Manipula a entrada de um Funcionário específico no banco de dados"""
    f = Funcionario.query.get(identifier)
    # Erro: Operação com funcionário não existente
    if not f:
        logger.log(request.method, "Funcionario<id>", "Erro: Funcionário não existente no banco de dados")
        abort(400)

    if request.method == "GET":
        logger.log("GET", "Funcionario<id>", "Funcionario {} retornado".format(f))
        return jsonify(f.serialize())

    elif request.method == "PUT":
        form = request.form
        changes = 0

        for attr in f.attributos:
            if attr in form:
                setattr(f, attr, form[attr])
                changes += 1
        if changes > 0:
            db.session.commit()
            logger.log("PUT", "Funcionario<id>",
                       "Funcionario {} atualizado e retornado com {} alteraçõe(s)".format(f, changes))
        else:
            logger.log("PUT", "Funcionario<id>",
                       "Funcionario {} retornado, com nenhum parametro fornecido para atualização".format(f))
        return jsonify(f.serialize())

    elif request.method == "DELETE":
        db.session.delete(f)
        db.session.commit()
        logger.log("DELETE", "Funcionario<id>", "Funcionario {} deletado".format(f))
        return jsonify(f.serialize())


########
# Main #
########
if __name__ == '__main__':
    app.run(host='localhost', debug=True)
