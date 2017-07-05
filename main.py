import cgi
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:developer@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(8000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner_id):
        self.name = name
        self.body = body
        self.owner_id = owner_id

#@app.before_request
#def require_login():
 #   allowed_routes = ['login', 'display_entries', 'index', 'add_user']
  #  if request.endpoint not in allowed_routes and 'username' not in session:
   #     return redirect('/login')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and User.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        elif User.password != password:
            flash('Password incorrect')
        else:
            flash('User does not exist')

    return render_template('login.html')

@app.route('/blog', methods=['GET'])
def display_entries():
    if request.args.get('id'):
        id = request.args.get('id')
        entry = Blog.query.filter_by(id=id).first()
        return render_template('blog_post.html', title='Build a Blog', entry=entry)
    else:
        entries = Blog.query.order_by(Blog.name.desc()).all()
        return render_template('blog.html', title='Build a Blog', entries=entries)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    error = False
    error1 = ""
    error2 = ""
    if request.method == 'POST':
        entry_name = request.form['entry']
        body_name = request.form['body']
        owner_id = Blog.owner_id
        if entry_name.strip() == "":
            error1 = "Please enter a title."
            error = True
        if body_name.strip() == "":
            error2 = "Please enter a body."
            error = True
        if error == True:
            return render_template('newpost.html', title='Build a Blog', error1=error1, error2=error2)
        
        new_post = Blog(entry_name, body_name, owner_id)
        db.session.add(new_post)
        db.session.commit()
        new_id = str(new_post.id)
        new_url = ('/blog?id=' + new_id)
        return redirect(new_url)
    
    else:
        return render_template('newpost.html', title='Blogz')

@app.route('/signup', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        new_user = request.form['username']
        new_password = request.form['password']
        pw_verify = request.form['verify']
        existing_user = User.query.filter_by(username=new_user).first()
        invalid_user = None
        invalid_pw = None
        pw_mismatch = None
        blank_field = None
        duplicate_user = None
        errors = False
    
        if (not new_user or new_user.strip() == "") or (not new_password or new_password.strip() == "") or (not pw_verify or pw_verify.strip() == ""):
            blank_field = "One or more fields is empty"
            errors = True

        if existing_user:
            duplicate_user = "Username already exists"
            new_user = ""
            errors = True

        if (not new_user) or (new_user.strip() == "") or (len(new_user) < 3) or (len(new_user) > 30) or (" " in new_user):
            invalid_user = "Please enter a valid username. Your username must be at least 3 and no longer than 30 characters and may not contain spaces."
            new_user = ""
            errors = True

        if (not new_password) or (new_password.strip() == "") or (len(new_password) < 3) or (len(new_password) > 30) or (" " in new_password):
            invalid_pw= "Please enter a password. Your password must be at least 3 and no longer than 30 characters and may not contain spaces."
            errors = True

        if (not pw_verify) or (pw_verify.strip() == "") or (new_password) != (pw_verify):
            pw_mismatch = "Please confirm your password."
            errors = True

        if (errors == False):
            new_user = cgi.escape(new_user, quote=True)
            return redirect('/newpost')
    
        else:
            return render_template('signup.html', username=new_user, invalid_user=invalid_user, invalid_pw=invalid_pw, pw_mismatch=pw_mismatch, blank_field=blank_field, duplicate_user=duplicate_user)

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()