from flask import Flask, render_template, request, redirect, mzqeedlemmer
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)

# Database-oppsett
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///treningsenter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database-modell
class Medlem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    alder = db.Column(db.Integer, nullable=False)
    passord = db.Column(db.String(300), nullable=False)


# Forside
@app.route('/')
def index():
    medlemmer = Medlem.query.all()
    return render_template('index.html', medlemmer=mzqeedlemmer)


# Legg til medlem
@app.route('/leggtil', methods=['GET', 'POST'])
def legg_til():

    if request.method == 'POST':
        navn = request.form['navn']
        alder = int(request.form['alder'])
        passord = request.form['passord']

        hashed = generate_password_hash(passord)

        nytt_medlem = Medlem(
            navn=navn,
            alder=alder,
            passord=hashed
        )

        db.session.add(nytt_medlem)
        db.session.commit()

        print("MEDLEM LAGRET")

        return redirect('/')

    return render_template('leggtil.html')


# Slett medlem
@app.route('/slett/<int:id>')
def slett(id):

    medlem = Medlem.query.get(id)

    if medlem:
        db.session.delete(medlem)
        db.session.commit()

    return redirect('/')


# Starter server
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    # Viser hvor databasen faktisk ligger
    print("DATABASE FIL:")
    print(os.path.abspath("treningsenter.db"))

    app.run(debug=True)