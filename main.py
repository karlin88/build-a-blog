from flask import Flask, request, url_for,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Test1234!@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key = True, unique = True)
    blog_name = db.Column(db.String(120))
    extracted_text = db.Column(db.text)
    image_path = db.Column(db.string(500))

    def __init__(self, blog_name, extracted_text = '',image_path = ''):
        self.blog_name = blog_name
        self.extracted_text = extracted_text
        self.image_path = image_path

class BlogPostHashTags(db.Model):
    hash_id = db.Column(db.Integer, db.ForeignKey('HashTags.hash_id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('Blog.blog_id'))

    def __init__(self):


class HashTags(db.Model):
    hash_id = db.Column(db.Integer, primary_key = True, unique = True)
    hash_name = db.Column(db.String(120))

    def __init__(self,hash_name):
        self.hash_name = hash_name


@app.route("/")
def index():
    return render_template('boilerplate.html')

if __name__ == '__main__':
    app.run()