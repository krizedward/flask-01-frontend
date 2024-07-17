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
    select_query = """
    SELECT * FROM pbuss_baru WHERE kode IN (
    '2020070271', '2020070264', '2019072086', '2022071451',
    '2023070429', '2017072211', '2017070670', '2016070021',
    '2017071142', '2016070474', '2024070107', '2018072599',
    '2017072550', '2017072031', '2017070595', '2017070346',
    '2016070059', '2016070028', '2017071693', '2023070431',
    '2016070538', '2017071874', '2016070301', '2022071527',
    '2023071368', '2016070403', '2014070565', '2019072926',
    '2014070031', '2020070620', '2020070619', '2019072436',
    '2016070156', '2019072242', '2014070380', '2019070094',
    '2019071439', '2014070734', '2020070537', '2019072043',
    '2019070661', '2019071119', '2022071205', '2019072936',
    '2019071823', '2015070589', '2014070158', '2014070516',
    '2014070555', '2015070017', '2019070158', '2021071266',
    '2019071700', '2022071950', '2022070511', '2022071566',
    '2022071566', '2022071248', '2022071736', '2022071487',
    '2022071257', '2022071957', '2022071953', '2022070697',
    '2022070515', '2022071475', '2023071885', '2023071060',
    '2023071078', '2023071598', '2023071815', '2023071886',
    '2023071425', '2023071007', '2022071460', '2022071469',
    '2022071471', '2022071485', '2022071962'
    );
    """
    cursor.execute(select_query)
    # cursor.execute('SELECT * FROM pbuss')
    data = cursor.fetchall()
    cursor.close()
    return data

def get_data_pbuss_old():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    select_query = """
    SELECT 
        pbuss.id,
        pbuss.buss,
        pbuss.nama,
        pbuss.no_buss,
        pbuss.nomor_surat_sekolah,
        pbuss.sekolah,
        pbuss.us,
        pbuss.us_buss,
        pbuss.kode,
        skh.nama_sekolah AS nama_sekolah,
        edu.kelas AS nama_kelas,
        CASE 
            WHEN kpd.orang_tua = 'Ayah' THEN cnt_alamat_ayah.alamat
            WHEN kpd.orang_tua = 'Ibu' THEN cnt_alamat_ibu.alamat
            WHEN kpd.orang_tua = 'Wali' THEN cnt_alamat_wali.alamat
        END AS almt,
        CASE 
            WHEN kpd.orang_tua = 'Ayah' THEN 'Bapak'
            WHEN kpd.orang_tua = 'Ibu' THEN 'Ibu'
            WHEN kpd.orang_tua = 'Wali' THEN 'Bapak/Ibu'
        END AS ortu_murid,
        CASE 
            WHEN kpd.orang_tua = 'Ayah' THEN cnt_ayah.nama
            WHEN kpd.orang_tua = 'Ibu' THEN cnt_ibu.nama
            WHEN kpd.orang_tua = 'Wali' THEN cnt_wali.nama
        END AS nama_ortu
    FROM pbuss
    JOIN education edu ON pbuss.kode = edu.kode
    JOIN sekolah skh ON edu.sekolah = skh.kode_sekolah
    JOIN kepada kpd ON kpd.no_buss = pbuss.no_buss
    LEFT JOIN contact cnt_alamat_ayah ON cnt_alamat_ayah.kode = pbuss.kode AND cnt_alamat_ayah.ortu = 'Ayah'
    LEFT JOIN contact cnt_alamat_ibu ON cnt_alamat_ibu.kode = pbuss.kode AND cnt_alamat_ibu.ortu = 'Ibu'
    LEFT JOIN contact cnt_alamat_wali ON cnt_alamat_wali.kode = pbuss.kode AND cnt_alamat_wali.ortu = 'Wali'
    LEFT JOIN contact cnt_ayah ON cnt_ayah.kode = pbuss.kode AND cnt_ayah.ortu = 'Ayah'
    LEFT JOIN contact cnt_ibu ON cnt_ibu.kode = pbuss.kode AND cnt_ibu.ortu = 'Ibu'
    LEFT JOIN contact cnt_wali ON cnt_wali.kode = pbuss.kode AND cnt_wali.ortu = 'Wali'
    """
    cursor.execute(select_query)
    # cursor.execute('SELECT * FROM pbuss')
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