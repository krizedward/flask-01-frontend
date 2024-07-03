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

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user

def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    db.commit()
    cursor.close()

# accounting
def get_data_accounting():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM accounting')
    data = cursor.fetchall()
    cursor.close()
    return data

def add_data_accounting(transaction_date, transaction_amount, transaction_description):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('INSERT INTO accounting (transaction_date, transaction_amount, transaction_description) VALUES (%s, %s, %s)', (transaction_date, transaction_amount, transaction_description))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()

def get_accounting_by_id(get_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM accounting WHERE id = %s', (get_id,))
    data = cursor.fetchone()
    cursor.close()
    return data

def delete_data_accounting(get_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('DELETE FROM accounting WHERE id = %s', (get_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
