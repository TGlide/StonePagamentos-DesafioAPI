from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

############################################
# Configurações do app e do Banco de Dados #
############################################
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' # Configuração básica - Não requer PostgreSQL
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postlogin369@localhost:1506/stone_DB'  # Usando PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Inicializa Banco de Dados


###########
# Modelos #
###########
class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    cargo = db.Column(db.String(128), nullable=False)
    idade = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Funcionário %r>' % self.nome

    def serialize(self):
        """Retorna a instância de Funcionário em formato serializável"""
        return {
            'id': self.id,
            'nome': self.nome,
            'cargo': self.cargo,
            'idade': self.idade
        }


#########
# Rotas #
#########
@app.route('/', methods=['GET'])
def home():
    return '<h1>Bem-vindo a API desafiadora da Stone Pagamentos!</h1>' \
           '<p>Thomas G. Lopes</p>'


@app.route('/api/v1/funcionarios', methods=['GET'])
def funcionarios_get():
    func_lista = [func.serialize() for func in
                  Funcionario.query.all()]  # Cria lista de todos os funcionários em formato serializável
    return jsonify(func_lista)


@app.route('/api/v1/funcionarios', methods=['POST'])
def funcionarios_post():
    return


########
# Main #
########
if __name__ == '__main__':
    app.run()
