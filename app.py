from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:developer@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'b\xed\xf8r\xf7\xa1\xe0*\x90.\x85\xd90\xae\xd8\n\xb4\xbc\x9db\xd6/\x92\x91\xf2'
