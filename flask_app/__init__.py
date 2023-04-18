from flask import Flask
app = Flask(__name__)
app.secret_key = "lrac"
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
DATABASE = "login_reg"
 