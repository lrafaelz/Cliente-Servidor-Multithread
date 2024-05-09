from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db = SQLAlchemy(app)

class DadosFormulario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    mensagem = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form['nome']
    mensagem = request.form['mensagem']
    novo_dado = DadosFormulario(nome=nome, mensagem=mensagem)
    db.session.add(novo_dado)
    db.session.commit()
    # dados do formulario:
    print(f'Nome: {nome}')
    print(f'Mensagem: {mensagem}')

    # Aqui você pode chamar seu código existente passando os parâmetros coletados
    # Por exemplo: seu_codigo(nome, mensagem)

    return render_template('formulario.html', nome=novo_dado.nome, mensagem=novo_dado.mensagem)

if __name__ == '__main__':
    app.run(debug=True)
