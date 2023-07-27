from flask import Flask, render_template, request, redirect, url_for, flash
from classes.userdb import UserDB
import classes.coupondb as CouponDB
import uuid, json

app = Flask(__name__, static_folder="./static")
app.config["SECRET_KEY"] = str(uuid.uuid4().hex)
#UserDB().reset()

@app.route("/login", methods=["GET", "POST"])
def login(): # ログイン画面
  if request.method == "GET":
    return render_template("login.html")
  else:
    email = request.form["email"]
    password = request.form["password"] # get email & password
    user = UserDB(email, password)
    user_id = user.getid_byemail()

    if user.logincheck():
      return redirect(url_for("home", id=user_id)) # 登録成功 -> idのurlに飛ぶ
    else:
      flash("入力が正しくありません")
      return redirect(url_for("login"))



@app.route("/account", methods=["GET", "POST"])
def account(): # アカウント登録
  if request.method == "GET":
    return render_template("account.html")
  else:
    email = request.form["email"]
    password = request.form["password"] # get email & password
    user = UserDB(email, password)

    if user.emailcheck(): # 有効なemailかcheck
      user.insert()
      CouponDB.create_table(user.id)
      return redirect(url_for("home", id=user.id)) # 登録成功 -> DB登録
    else:
      flash('このメールアドレスは既に使われているか、使用できません')
      return redirect(url_for("account"))



@app.route("/home/<string:id>", methods=["GET", "POST"])
def home(id):
    if request.method == "GET":
      user_data = json.loads(CouponDB.select_db(id))
      return render_template("home.html", user_data=user_data)
    else:
      return render_template("home.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8930, debug=True)