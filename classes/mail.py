from flask import Flask
from flask_mail import Mail, Message

def create_flask_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587  # TLSは587、SSLなら465
    app.config['MAIL_USERNAME'] = 'qpon.go.u19@gmail.com'
    app.config['MAIL_PASSWORD'] = 'odeyhsdogvvoqcmf'  # Gmailのmail用のmパスワード設定をしておく必要あり
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = 'qpon.go.u19@gmail.com'  # これがあるとsender設定が不要になる
    f_mail = Mail(app)

    @app.route('/mail')
    def send_mail():
        msg = Message('Test Mail', recipients=['musashinonh2022@gmail.com'])
        msg.body = "Hello Flask message sent from Flask-Mail"
        f_mail.send(msg)
        return None