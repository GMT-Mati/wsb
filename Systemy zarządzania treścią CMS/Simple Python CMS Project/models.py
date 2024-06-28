from werkzeug.security import generate_password_hash, check_password_hash
from database import connect_db

class User:
    @staticmethod
    def create(username, password):
        hashed_password = generate_password_hash(password)
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()

    @staticmethod
    def authenticate(username, password):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user[2], password):
                return user
            return None

class Article:
    @staticmethod
    def create(title, content, author_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO articles (title, content, author_id) VALUES (?, ?, ?)', (title, content, author_id))
            conn.commit()

    @staticmethod
    def get_all():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT articles.*, users.username FROM articles JOIN users ON articles.author_id = users.id')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(article_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM articles WHERE id = ?', (article_id,))
            return cursor.fetchone()

    @staticmethod
    def update(article_id, title, content):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE articles SET title = ?, content = ? WHERE id = ?', (title, content, article_id))
            conn.commit()

    @staticmethod
    def delete(article_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM articles WHERE id = ?', (article_id,))
            conn.commit()
