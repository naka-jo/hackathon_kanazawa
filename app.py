from flask import Flask, render_template, request

app = Flask(__name__, static_folder="./static")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
      return render_template("login.html")

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "GET":
      return render_template("account.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
      return render_template("home.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8930, debug=True)