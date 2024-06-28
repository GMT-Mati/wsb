from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from database import create_tables
from models import User, Article

app = Flask(__name__)
app.secret_key = 'your_secret_key'
Bootstrap(app)

create_tables()

@app.route('/')
def index():
    articles = Article.get_all()
    return render_template('index.html', articles=articles)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create(username, password)
        flash('User registered successfully!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create_article():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = session['user_id']
        Article.create(title, content, author_id)
        return redirect(url_for('index'))
    return render_template('create_article.html')

@app.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    article = Article.get_by_id(article_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        Article.update(article_id, title, content)
        return redirect(url_for('index'))
    return render_template('edit_article.html', article=article)

@app.route('/delete/<int:article_id>')
def delete_article(article_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    Article.delete(article_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
