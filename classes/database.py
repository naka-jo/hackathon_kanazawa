import sqlite3

def create_table(dbname):
    conn = sqlite3.connect(f'../database/{dbname}')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS coupon_table(data TEXT, discount TEXT, store TEXT, category TEXT, remarks TEXT);'
    )
    conn.commit()
    conn.close()

def insert_db(dbname, data):
    conn = sqlite3.connect(f'../database/{dbname}')
    cur = conn.cursor()
    cur.execute('INSERT INTO coupon_table(data, discount, store, category, remarks) values(?, ?, ?, ?, ?);', data)
    conn.commit()
    conn.close()
    
def select_db(dbname):
    conn = sqlite3.connect(f'../database/{dbname}')
    cur = conn.cursor()
    cur.execute('SELECT * FROM coupon_table;')
    result = cur.fetchall()
    conn.close()
    return result

dbname = 'hiroyuki'
create_table(dbname)
data = ['7/30', '50円引き', 'なか卯', '飲食', None]
insert_db(dbname, data)
result = select_db(dbname)
print(result)