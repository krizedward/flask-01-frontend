from .db import get_db

def get_all_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return users

def add_user(username, email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (username, email) VALUES (%s, %s)', (username, email))
    db.commit()
    cursor.close()
