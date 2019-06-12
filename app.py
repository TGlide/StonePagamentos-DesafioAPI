from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

from logger import Logger

############################################
# Configurações do app e do Banco de Dados #
############################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # Configuração básica - Não requer PostgreSQL
# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postlogin369@localhost:1506/stone_DB'  # Usando PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Inicializa Banco de Dados
logger = Logger()


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
        func_lista = [func.serialize() for func in
                      Funcionario.query.all()]  # Cria lista de todos os funcionários em formato serializável
        logger.log("GET", "Funcionario", "{} iten(s) foram retornados (Sem filtros)".format(len(func_lista)))
        return jsonify(func_lista)

    elif request.method == 'POST':
        f = Funcionario()
        if not request.form:
            abort(400)  # TODO: Display and log error
        try:
            f.nome = request.form['nome']
            f.idade = int(request.form['idade'])
            f.cargo = request.form['cargo']
        except Exception as e:
            abort(400)  # TODO: Log error
        else:
            db.session.add(f)
            db.session.commit()
            logger.log("POST", "Funcionario", "Add Funcionário {}".format(f))
            return jsonify(f.serialize())


@app.route('/api/v1/funcionarios/<int:identifier>', methods=['GET', 'PUT', 'DELETE'])
def funcionarios_id(identifier):
    """Manipula a entrada de um Funcionário específico no banco de dados"""
    f = Funcionario.query.get(identifier)
    if not f:
        logger.log(request.method, "Funcionario<id>", "Erro > Funcionário não existente no banco de dados")
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


########
# Main #
########
if __name__ == '__main__':
    app.run(debug=True)
