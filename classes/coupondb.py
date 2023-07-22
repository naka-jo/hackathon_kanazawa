import sqlite3

def create_table(dbname):
    conn = sqlite3.connect(f'../database/{dbname}')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS coupon_table(id INTEGER PRIMARY KEY, data TEXT, discount TEXT, store TEXT, category TEXT, remarks TEXT);'
    )
    conn.commit()
    conn.close()

def insert_db(dbname, data):
    conn = sqlite3.connect(f'../database/{dbname}')
    cur = conn.cursor()
    cur.execute('INSERT INTO coupon_table(id, data, discount, store, category, remarks) values(?, ?, ?, ?, ?, ?);', data)
    conn.commit()
    conn.close()
    
def select_db(dbname):
    conn = sqlite3.connect(f'../database/{dbname}')
    cur = conn.cursor()
    cur.execute('SELECT * FROM coupon_table;')
    result = cur.fetchall()
    conn.close()
    return result

def delete_column(dbname, id):
    conn = sqlite3.connect(f'../database/{dbname}')
    cur = conn.cursor()
    cur.execute(f'DELETE FROM coupon_table WHERE id={id};')
    conn.commit()
    conn.close()

# dbname = 'hiroyuki'
# create_table(dbname)
# data = [None, '7/30', '50円引き', 'なか卯', '飲食', None]
# data = [None, '8/3', '10%off', 'スターバックス', '飲食', None]
# insert_db(dbname, data)
# delete_column(dbname, 1)
# result = select_db(dbname)
# print(result)