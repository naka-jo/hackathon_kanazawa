import sqlite3
import uuid
from email_validator import *

class UserDB:
    def __init__(self, email=None, password=None):
        self.con = sqlite3.connect('./database/users.db')
        self.cur = self.con.cursor()

        self.id = str(uuid.uuid4()).split("-")[-1] # id自動生成
        self.email = email
        self.password = password


    def get(self): # DBから全ての要素を取得し、1人分{id: ,email: ,password: }の辞書で返す
        self.cur.execute('SELECT * FROM USERS;')
        userdb = [{"email":i[1] ,"password":i[2]} for i in self.cur]
        return userdb
    
    def getid_byemail(self): # emailからidを取得
        self.cur.execute('SELECT id FROM USERS WHERE email = ? ;', (self.email,))
        return list(self.cur)[0][0]

    def logincheck(self): # ログイン時に入力情報が正しいかチェック
        userdb = self.get()
        input = {"email":self.email, "password":self.password}
        if input in userdb:
            return True
        else:
            return False


    def emailcheck(self): # アカウント登録時にメールアドレスをチェック
        try: # メールアドレスかどうかチェック
            validate_email(self.email, check_deliverability=False)
        except:
            return False
        else: # すでに使われていないかチェック
            self.cur.execute("SELECT * FROM USERS WHERE email = ?;", (self.email,))
            if len(list(self.cur)) == 0:
                return True
            else:
                return False
    

    def insert(self): # DBにユーザーを追加
        user = (self.id, self.email, self.password)
        self.cur.execute('INSERT INTO USERS values(?,?,?);', user)
        self.con.commit()
        

    def reset(self): # DBの初期化
        self.cur.execute("DROP TABLE IF EXISTS USERS;")
        self.cur.execute("CREATE TABLE USERS (\
        id TEXT UNIQUE NOT NULL, \
        email TEXT UNIQUE NOT NULL, \
        password TEXT NOT NULL);")    


    def close(self): # connect.close() SQL実行後必ず動かす
        self.con.close()


if __name__ == "__main__":
    db = UserDB("example@ac.jp", "aiueo1234")
    # db.insert()
    print(list(db.getid_byemail())[0][0])
