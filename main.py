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

def doesnotexist(string):
    if not string or string.strip() == "":
        return True
    else:
        return False

def convertstrtoblank(string):
    if string is None:
        return ''
    else:
        return string

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
    t_error = ""
    b_error = ""

    if doesnotexist(title):
        t_error = "Please fill in the title"
    
    if doesnotexist(postbody):
        b_error = "Please fill in the body"
    
    #return render_template('blog.html', blog = get_blogs())
    if doesnotexist(t_error) and doesnotexist(b_error):
        blog = Blog(title, postbody, image)
        db.session.add(blog)
        db.session.commit()
        return redirect ("/?id=" + str(blog.id))
    else:
        return render_template('newpost.html',
            title_error = convertstrtoblank(t_error),
            body_error = convertstrtoblank(b_error)
        )


if __name__ == "__main__":
    app.run()
