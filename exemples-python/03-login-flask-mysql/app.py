# pip3 install Flask
# pip3 install flask-login
# pip3 install mysql-connector-python

# CREATE TABLE users (
#   id int(10) unsigned NOT NULL AUTO_INCREMENT,
#   email varchar(255) DEFAULT NULL,
#   password varchar(256),
#   PRIMARY KEY (id),
#   UNIQUE KEY email (email)
# );

# INSERT INTO users (email, password) VALUES ('joe@gmail.com',SHA2('joe123', 256));

import logging
import mysql.connector as mysql
from flask import Flask, request, redirect, abort, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

con = mysql.connect(database="mysql", user="root", password="demo", host="127.0.0.1", port="3306")
cur = con.cursor()

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

#SECRET_KEY: clau d'encriptació de la cookie
app.config.update(
    SECRET_KEY='secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

    def __repr__(self):
        return f"{self.id}:{self.email}"

# contingut protegit tan sols per a usuaris registrats
@app.route('/')
@login_required
def home():
    app.logger.info(f"Usuari id = {current_user.id} & email = {current_user.email}")
    return render_template('home.html', user=current_user.email)

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email_introduit = request.form['email']
        password_introduit = request.form['password']

        #consulto a la base de dades si tot és correcte
        cur.execute(f"""
            SELECT id 
            FROM users
            WHERE email = '{email_introduit}' 
            AND password = SHA2('{password_introduit}', 256)
        """)

        row = cur.fetchone()
        if row is None:
            # usuari/password incorrectes
            return abort(401)
        else:
            user = User(id = int(row[0]), email = email_introduit)
            login_user(user)
            return redirect("/")
    else:
        return render_template('login.html', message="Si us plau, introduexi les seves credencials")

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login.html', message="S'ha desconnectat amb éxit")

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return render_template('login.html', message="Error d'autenticació. Torni a provar-ho")

# callback to reload the user object
@login_manager.user_loader
def load_user(str_id):
    # flask-login fa considera els id com str
    id=int(str_id)
    
    #busco en base de dades l'usuari
    cur.execute(f"""select email from users where id = {id}""")
    row = cur.fetchone()

    if row is None:
        # no existeix l'usuari a la base de dades
        return None
    else:
        return User(id = id, email = row[0])

# Necessari per iniciar un servidor de proves
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
