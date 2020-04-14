import os
from flask_mail import Message
from flask import url_for
from shellmancer import mail


def send_verify_email(user):
    token = user.get_token(expires_sec=3600)
    msg = Message("Verify Your New Account @ Shellmancer",
                  sender=os.environ['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f"An account for {user.email} at shellmancer.herokuapp.com needs verification." \
        + f"Click here to verify account: {url_for('verify_success', token=token, _external=True)}" \
        + " Ignore this message if it was sent in error."
    mail.send(msg)

def send_reset_email(user):
    token = user.get_token(expires_sec=1800)
    msg = Message("Password Reset Request @ Shellmancer",
                  sender=os.environ['MAIL_USERNAME'], recipients=[user.email])
    msg.body = "To reset your password, visit the following link:" \
        + f"{url_for('reset_password', token=token, _external=True)}"
    mail.send(msg)

