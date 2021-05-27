from threading import Thread
from flask import render_template, current_app, jsonify
from flask import Blueprint
from flask_mail import Mail, Message
from .. import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail_promo(itens):
    msg = Message('[JARBAS] - Melhores Preços', sender = 'news@jarbas.com.br', recipients = ['someone1@gmail.com'])
    msg.html = render_template('home/email.html', itens=itens)
    app = current_app._get_current_object()
    Thread(target=send_async_email, args=(app, msg)).start()

def send_mail_reset(token, user=None):
    msg = Message('[JARBAS] - Reset de senha', sender = 'news@jarbas.com.br', recipients = ['someone1@gmail.com'])
    msg.html = render_template('auth/email_reset_password.html', token=token, user=user)
    app = current_app._get_current_object()
    Thread(target=send_async_email, args=(app, msg)).start()