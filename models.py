from app import db
from hashutils import make_pw_hash, make_salt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    pw_hash = db.Column(db.String(30))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, pw_hash):
        self.username = username
        self.pw_hash = make_pw_hash(pw_hash)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(8000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner_id = owner