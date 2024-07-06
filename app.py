## importando as principais bibliotecas e frameworks


from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Pessoa(db.Model):
    __tablename__ = 'cliente'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    cpf = db.Column(db.String(11))
    email = db.Column(db.String(100))

    def __init__(self, nome, telefone, cpf, email):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.email = email

with app.app_context():
    db.create_all()

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/cadastrar')
def cadastrar():
    return render_template("cadastro.html")

@app.route('/cadastro',methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        cpf = request.form.get("cpf")
        email = request.form.get("email")

        if nome and telefone and cpf and email:
            p = Pessoa(nome, telefone, cpf, email)
            db.session.add(p)
            db.session.commit()

    return redirect(url_for("index"))

@app.route('/lista')
def lista():
    pessoas = Pessoa.query.all()
    return render_template('lista.html', pessoas=pessoas)

@app.route('/excluir/<int:id>')
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
    if pessoa:
        db.session.delete(pessoa)
        db.session.commit()

    return redirect(url_for('lista'))

@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
    if not pessoa:
        return redirect(url_for('lista'))

    if request.method == 'POST':
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        email = request.form.get("email")

        if nome and telefone and email:
            pessoa.nome = nome
            pessoa.telefone = telefone
            pessoa.email = email
            db.session.commit()

            return redirect(url_for('lista'))

    return render_template('atualizar.html', pessoa=pessoa)

if __name__ == '__main__':
    app.run(debug=True)
