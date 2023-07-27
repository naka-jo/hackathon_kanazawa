import sqlite3
import json

def create_table(table): # テーブルを作成
    conn = sqlite3.connect(f"../database/coupon.db")
    cur = conn.cursor()
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table}(id INTEGER PRIMARY KEY, data TEXT, discount TEXT, store TEXT, category TEXT, remarks TEXT);"
    )
    conn.commit()
    conn.close()

def insert_db(table, data): # データを追加
    conn = sqlite3.connect(f"../database/coupon.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table}(id, data, discount, store, category, remarks) values(?, ?, ?, ?, ?, ?);", data)
    conn.commit()
    conn.close()

def select_db(table): # データを取得
    conn = sqlite3.connect(f"../database/coupon.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table};")
    dict_values = cur.fetchall()
    conn.close()
    dict_keys = ("id", "日付", "割引", "店", "カテゴリー", "備考")
    result = []
    for values in dict_values:
        result_dict = {k: v for k, v in zip(dict_keys, values)}
        result.append(result_dict)
    with open(f'../database/json/{table}.json', 'w') as f:
        json.dump(result, f, indent=4, ensure_ascii = False)

def delete_table(table, id): # データを消去
    conn = sqlite3.connect(f"../database/coupon.db")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table} WHERE id={id};")
    conn.commit()
    conn.close()

# dbname = "coupon"
# table = "kanra"
# create_table(table)
# data = [None, "7/30", "50円引き", "なか卯", "飲食", None]
# data = [None, "8/3", "10%off", "スターバックス", "飲食", None]
# insert_db(table, data)
# delete_table(table, 3)
# result = select_db(table)
# print(result)