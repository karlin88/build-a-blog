from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
#'mysql+pymysql://build-a-blog:blogger@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    blogtitle = db.Column(db.String(120))
    body = db.Column(db.Text)
    imagepath = db.Column(db.String(120))

    def __init__(self, blogtitle, body, imagepath):
        self.blogtitle = blogtitle
        self.body = body
        self.imagepath = imagepath

    def __repr__(self):
        return '<Blog %r>' % self.blogtitle

def get_blogs():
    return Blog.query.order_by(Blog.id.desc()).all()

def get_singleblog(blogid):
    return Blog.query.filter_by(id = blogid)


@app.route("/")
def index():
    blogpost = request.args.get("id")
    if blogpost is None:
        blogs = get_blogs()
    else:
        blogs = get_singleblog(blogpost)
    return render_template('blog.html', blog = blogs)

@app.route("/newpost")
def newblogform():
    return render_template('newpost.html')

@app.route("/newpost", methods=['POST'])
def add_post():
    title = request.form['blogtitle']
    postbody = request.form['body']
    image = request.form['imagepath']

    blog = Blog(title, postbody, image)
    db.session.add(blog)
    db.session.commit()
    
    #return render_template('blog.html', blog = get_blogs())
    return redirect ("/?id=" + str(blog.id))


if __name__ == "__main__":
    app.run()
