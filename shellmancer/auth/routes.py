from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from shellmancer import db, ph
from shellmancer.models import UserAccount
from shellmancer.auth.utils import send_reset_email, send_verify_email
from argon2.exceptions import InvalidHash
from shellmancer.auth.forms import (
    RegisterForm, LoginForm, RequestResetForm, PasswordResetForm, RequestVerifyForm
)

auth = Blueprint('auth', 'shellmancer')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pw = ph.hash(form.password.data)
        user = UserAccount(email=form.email.data, password=hashed_pw)

        db.session.add(user)
        db.session.commit()

        send_verify_email(user)

        flash(f"Account created for {form.email.data}"
              + "Check your email to verify account for full functionality. You may login now.", 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html", title="Register", form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.player_profile'))

    form = LoginForm()

    if form.validate_on_submit():
        user = UserAccount.query.filter_by(email=form.email.data).first()
        try:
            if user and ph.verify(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
        except InvalidHash:
            flash('Login Unsuccessful. Please check email and password.', 'danger')

    return render_template("login.html",
                           title="Login",
                           form=form)


@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out. You can login again.', 'info')
        return redirect(url_for('auth.login'))

    else:
        return redirect(url_for('main.home'))



@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = UserAccount.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to submit your password", "info")
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title="Reset Password", form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = UserAccount.verify_token(token)
    if user is None:
        flash("That is an invalid token or it has expired.", 'warning')
        return redirect(url_for('auth.reset_request'))

    form = PasswordResetForm()
    if form.validate_on_submit():

        hashed_pw = ph.hash(form.password.data)
        user.password = hashed_pw
        db.session.commit()
        flash(f"Account password has been updated. You may login.", 'success')

        if not user.is_verified:
            user.is_verified = True
            db.session.commit()
            flash(f"Your account was verified in the process of password resetting.", 'success')

        return redirect(url_for('auth.login'))
    return render_template("reset_password.html", title="Confirm Password Reset", form=form)



@auth.route('/verify', methods=['GET', 'POST'])
@login_required
def verify_request():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if current_user.is_verified:
        flash('This account is already verified.', 'info')
        return redirect(url_for('users.player_profile'))

    form = RequestVerifyForm()
    if form.validate_on_submit():
        user = UserAccount.query.filter_by(email=current_user.email).first()
        send_verify_email(user)
        flash("An email has been sent with instructions to verify your account", "info")
        return redirect(url_for('users.player_profile'))

    return render_template('verify_request.html', title="Verify Account", form=form)


@auth.route('/verify/<token>')
def verify_success(token):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if current_user.is_verified:
        flash("Account is already verified", 'info')
        return redirect(url_for('users.player_profile'))

    user = UserAccount.verify_token(token)
    if user is None:
        flash("That is an invalid token or it has expired.", 'warning')
        return redirect(url_for('auth.verify_request'))

    if not user.is_verified:
        user.is_verified = True
        db.session.commit()
        flash(f"Your account was successfully verified.", 'success')

        return redirect(url_for('auth.login'))
    return render_template("reset_password.html", title="Confirm Password Reset", form=form)
