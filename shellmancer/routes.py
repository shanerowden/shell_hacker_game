import os
import secrets
from flask import render_template, flash, redirect, url_for, request
from shellmancer import app, db, ph
from shellmancer.forms import (
    RegisterForm, LoginForm, NewCampaignForm, UserSettingsForm, RequestResetForm, PasswordResetForm, RequestVerifyForm
)
from shellmancer.models import UserAccount, SinglePlayerCampaign
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from shellmancer.mailing import send_verify_email, send_reset_email
from argon2.exceptions import InvalidHash


@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pw = ph.hash(form.password.data)
        user = UserAccount(email=form.email.data, password=hashed_pw)

        db.session.add(user)
        db.session.commit()

        send_verify_email(user)

        flash(f"Account created for {form.email.data}"
              + "Check your email to verify account for full functionality. You may login now.", 'success')
        return redirect(url_for('login'))

    return render_template("register.html",
                           title="Register",
                           form=form)



@app.route('/verify', methods=['GET', 'POST'])
@login_required
def verify_request():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if current_user.is_verified:
        flash('This account is already verified.', 'info')
        return redirect(url_for('player_profile'))

    form = RequestVerifyForm()
    if form.validate_on_submit():
        user = UserAccount.query.filter_by(email=current_user.email).first()
        send_verify_email(user)
        flash("An email has been sent with instructions to verify your account", "info")
        return redirect(url_for('player_profile'))

    return render_template('verify_request.html', title="Verify Account", form=form)



@app.route('/verify/<token>')
def verify_success(token):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if current_user.is_verified:
        flash("Account is already verified", 'info')
        return redirect(url_for('player_profile'))

    user = UserAccount.verify_token(token)
    if user is None:
        flash("That is an invalid token or it has expired.", 'warning')
        return redirect(url_for('verify_request'))

    if not user.is_verified:
        user.is_verified = True
        db.session.commit()
        flash(f"Your account was successfully verified.", 'success')

        return redirect(url_for('login'))
    return render_template("reset_password.html", title="Confirm Password Reset", form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('player_profile'))

    form = LoginForm()

    if form.validate_on_submit():
        user = UserAccount.query.filter_by(email=form.email.data).first()
        try:
            if user and ph.verify(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
        except InvalidHash:
            flash('Login Unsuccessful. Please check email and password.', 'danger')

    return render_template("login.html",
                           title="Login",
                           form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out. You can login again.', 'info')
        return redirect(url_for('login'))

    else:
        return redirect(url_for('home'))



@app.route('/player')
@login_required
def player_profile():
    return render_template("player.html")


@app.route('/gamemaster')
@login_required
def gamemaster_profile():
    if current_user.gamemaster.gamemaster_access > 0:
        campaigns = SinglePlayerCampaign.query.filter_by(gamemaster_id=current_user.gamemaster.gamemaster_id)
        return render_template("gamemaster.html", campaigns=campaigns)
    else:
        flash("This user is not a gamemaster", 'info')
        return redirect(url_for('player_profile'))


@app.route('/gamemaster-make')
@login_required
def make_gamemaster():
    if current_user.gamemaster.gamemaster_access > 0:
        flash("User is already a game master", 'info')
        return redirect(url_for('gamemaster_profile'))
    else:
        current_user.gamemaster.gamemaster_access = 1
        db.session.add(current_user)
        db.session.commit()
        flash("{{current_user.email}} set to gamemaster.")
        return redirect(url_for('gamemaster_profile'))


@app.route('/new_campaign', methods=['GET', 'POST'])
@login_required
def new_campaign():
    if not current_user.gamemaster.gamemaster_access > 0:
        return redirect(url_for('player_profile'))
    else:
        form = NewCampaignForm()
        if form.validate_on_submit():
            campaign = SinglePlayerCampaign(gamemaster_id=current_user.gamemaster.gamemaster_id,
                                            campaign_name=form.title.data,
                                            campaign_descrip=form.descrip.data)
            db.session.add(campaign)
            db.session.commit()
            return redirect(url_for('gamemaster_profile'))
    return render_template("campaign_new.html",
                           form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/img/pfp', picture_fn)

    # resize
    basewidth = 128
    img = Image.open(form_picture)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize))

    img.save(picture_path)
    return picture_fn


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = UserSettingsForm()
    if form.validate_on_submit():

        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file

        if form.email.data != current_user.email:
            current_user.is_verified = False
            flash('Your verified status is now pending verification of the new email.', 'warning')

        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        current_user.is_over_18 = form.is_over_18.data
        db.session.commit()
        flash("Your account has been updated", 'success')
        return redirect(url_for('user_settings'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
        form.is_over_18.data = current_user.is_over_18
    return render_template('settings.html',
                           title=f"Settings for {current_user.email}",
                           form=form)

@app.route('/campaigns')
def all_campaigns():
    campaigns = SinglePlayerCampaign.query.all()
    campaigns.reverse()
    return render_template('campaigns.html',
                           title="All Campaigns", campaigns=campaigns)


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = UserAccount.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to submit your password", "info")
        return redirect(url_for('login'))
    return render_template('reset_request.html', title="Reset Password", form=form)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = UserAccount.verify_token(token)
    if user is None:
        flash("That is an invalid token or it has expired.", 'warning')
        return redirect(url_for('reset_request'))

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

        return redirect(url_for('login'))
    return render_template("reset_password.html", title="Confirm Password Reset", form=form)


@app.route('/docs')
def docs():
    return render_template("docs.html")


