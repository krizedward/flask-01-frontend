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

def update_accounting(accounting_id, transaction_date=None, transaction_amount=None, transaction_description=None):
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Membuat daftar kolom yang akan diperbarui
        fields = []
        values = []

        if transaction_date is not None:
            fields.append('transaction_date = %s')
            values.append(transaction_date)
        
        if transaction_amount is not None:
            fields.append('transaction_amount = %s')
            values.append(transaction_amount)
        
        if transaction_description is not None:
            fields.append('transaction_description = %s')
            values.append(transaction_description)
        
        values.append(accounting_id)
        
        # Menggabungkan string query
        query = f"UPDATE accounting SET {', '.join(fields)} WHERE id = %s"
        
        # Menjalankan query
        cursor.execute(query, values)
        db.commit()
        print(f"Record with id {accounting_id} updated successfully")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
        print("Database connection closed")

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

# inventory
def get_data_inventorys():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM inventory')
    data = cursor.fetchall()
    cursor.close()
    return data

def add_data_inventorys(transaction_date, transaction_amount, transaction_description):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('INSERT INTO inventory (transaction_date, transaction_amount, transaction_description) VALUES (%s, %s, %s)', (transaction_date, transaction_amount, transaction_description))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()

def get_inventorys_by_id(get_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM inventory WHERE id = %s', (get_id,))
    data = cursor.fetchone()
    cursor.close()
    return data

def update_inventorys(accounting_id, transaction_date=None, transaction_amount=None, transaction_description=None):
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Membuat daftar kolom yang akan diperbarui
        fields = []
        values = []

        if transaction_date is not None:
            fields.append('transaction_date = %s')
            values.append(transaction_date)
        
        if transaction_amount is not None:
            fields.append('transaction_amount = %s')
            values.append(transaction_amount)
        
        if transaction_description is not None:
            fields.append('transaction_description = %s')
            values.append(transaction_description)
        
        values.append(accounting_id)
        
        # Menggabungkan string query
        query = f"UPDATE accounting SET {', '.join(fields)} WHERE id = %s"
        
        # Menjalankan query
        cursor.execute(query, values)
        db.commit()
        print(f"Record with id {accounting_id} updated successfully")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
        print("Database connection closed")

def delete_data_inventorys(get_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('DELETE FROM inventory WHERE id = %s', (get_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()

# pbuss

def get_data_pbuss():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM pbuss')
    data = cursor.fetchall()
    cursor.close()
    return data

def get_pbuss_by_kode(get_kode):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM pbuss WHERE kode = %s', (get_kode,))
    data = cursor.fetchone()
    cursor.close()
    return data