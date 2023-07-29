from flask import Flask, render_template, request, redirect, url_for, flash
from classes.userdb import UserDB
import classes.coupondb as CouponDB
from classes.Image_to_Text import image_to_text
import uuid, json, os, base64, shutil

app = Flask(__name__, static_folder="./static")
app.config["SECRET_KEY"] = str(uuid.uuid4().hex)
# UserDB().reset()
# if os.path.exists("./database/coupon.db"):
#   CouponDB.drop_db()


@app.route("/login", methods=["GET", "POST"])
def login(): # ログイン画面
  if request.method == "GET":
    return render_template("login.html")
  else:
    email = request.form["email"]
    password = request.form["password"] # get email & password
    user = UserDB(email, password)

    if user.logincheck():
      user_id = user.getid_byemail()
      return redirect(url_for("home", id=user_id)) # 登録成功 -> idのurlに飛ぶ
    else:
      flash("※入力が正しくありません")
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



@app.route("/coupon", methods=["GET", "POST"])
def coupon(): # クーポン登録画面
    if request.method == "GET":
      return render_template("coupon.html")
    else:
      images = request.files.getlist("image")
      for image in images:
        image.save(os.path.join("./cloud",image.filename))
      if 0 < len(os.listdir("./cloud")) <= 2:
        return redirect(url_for("coupon2"))
      else:
        shutil.rmtree("./cloud")
        os.mkdir("./cloud")
        flash("写真数が適切ではありません。リロードしてやり直してください")
        return redirect(url_for("coupon"))
        

@app.route("/camera", methods=["POST"])
def camera(): # カメラで撮影された画像を保存
    data = request.json
    if 'img' in data:
      image_data = base64.b64decode(data['img'])
      save_path = f"./cloud/{uuid.uuid4().hex}.jpg"
      with open(save_path, 'wb') as f:
          f.write(image_data)
      return redirect(url_for("coupon"))
    else:
      return redirect(url_for("coupon"))
      

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5596, debug=True)