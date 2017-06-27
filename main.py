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
        if entry_name.strip() == "":
            error1 = "Please enter a title."
            error = True
        if body_name.strip() == "":
            error2 = "Please enter a body."
            error = True
        if error == True:
            return render_template('newpost.html', title='Build a Blog', error1=error1, error2=error2)
        
        new_post = Blog(entry_name, body_name)
        db.session.add(new_post)
        db.session.commit()
        new_id = str(new_post.id)
        new_url = ('/blog?id=' + new_id)
        return redirect(new_url)
    
    else:
        return render_template('newpost.html', title='Build a Blog')
    
if __name__ == '__main__':
    app.run()