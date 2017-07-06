import cgi
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import User, Blog
from app import app, db
from hashutils import check_pw_hash, make_pw_hash

@app.before_request
def require_login():
    allowed_routes = ['login', 'display_entries', 'index', 'add_user']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if check_pw_hash(password, user.pw_hash):
                session['username'] = user.username
                flash("Logged in")
                return redirect('/newpost')
            elif user.pw_hash != check_pw_hash(password, user.pw_hash):
                flash('Password incorrect')
            else:
                flash('User does not exist')
        return redirect('/login')

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
    
    return render_template('newpost.html', title='Blogz')

@app.route('/signup', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        new_user = cgi.escape(request.form['username'], quote=True)
        new_password = cgi.escape(request.form['password'], quote=True)
        pw_verify = cgi.escape(request.form['verify'], quote=True)
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
            user = User(username=new_user, pw_hash=new_password)
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
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