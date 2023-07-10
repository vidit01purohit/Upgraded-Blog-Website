from flask import Flask, render_template, redirect
from allforms import ContactForm
import requests
import sqlite3

#Setting up sql connections
conn = sqlite3.connect('blogs.db',check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS blogcon (name varchar(30) PRIMARY KEY, email varchar(30), phone char(10), content varchar(150))')
conn.commit()

#Getting blog post from npoint API
response = requests.get("https://api.npoint.io/16c6e61097ddbb9a150c")
posts = response.json()

app = Flask(__name__)
app.secret_key = "some secret string"

@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact",methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email_id.data
        content = form.text.data
        phone = form.phone.data
        name = form.name.data
        conn.execute("INSERT INTO blogcon \
                    (name,email,phone,content) VALUES (?,?,?,?)",
                       (name, email, phone, content))
        conn.commit()
        return redirect('/')
    return render_template("contact.html", form=form)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)