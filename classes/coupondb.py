import sqlite3

def create_table(table):
    conn = sqlite3.connect(f'../database/coupon.db')
    cur = conn.cursor()
    cur.execute(
        f'CREATE TABLE IF NOT EXISTS {table}(id INTEGER PRIMARY KEY, data TEXT, discount TEXT, store TEXT, category TEXT, remarks TEXT);'
    )
    conn.commit()
    conn.close()

def insert_db(table, data):
    conn = sqlite3.connect(f'../database/coupon.db')
    cur = conn.cursor()
    cur.execute(f'INSERT INTO {table}(id, data, discount, store, category, remarks) values(?, ?, ?, ?, ?, ?);', data)
    conn.commit()
    conn.close()

def select_db(table):
    conn = sqlite3.connect(f'../database/coupon.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {table};')
    result = cur.fetchall()
    conn.close()
    return result

def delete_table(table, id):
    conn = sqlite3.connect(f'../database/coupon.db')
    cur = conn.cursor()
    cur.execute(f'DELETE FROM {table} WHERE id={id};')
    conn.commit()
    conn.close()

# dbname = 'coupon'
# table = 'kanra'
# create_table(dbname, table)
# data = [None, '7/30', '50円引き', 'なか卯', '飲食', None]
# data = [None, '8/3', '10%off', 'スターバックス', '飲食', None]
# insert_db(dbname, table, data)
# delete_table(dbname, table, 3)
# result = select_db(dbname, table)
# print(result)