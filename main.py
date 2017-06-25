from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:developer@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(8000))

    def __init__(self, name, body):
        self.name = name
        self.body = body


        
@app.route('/blog', methods=['GET'])
def display_entries():
    entries = Blog.query.all()
    return render_template('blog.html', title='Build a Blog', entries=entries)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        entry_name = request.form['entry']
        body_name = request.form['body']
        new_post = Blog(entry_name, body_name)
        db.session.add(new_post)
        db.session.commit()
    else:
        return render_template('newpost.html', title='Build a Blog')

    return redirect ('/blog')

if __name__ == '__main__':
    app.run()