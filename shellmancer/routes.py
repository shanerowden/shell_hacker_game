import os
import secrets
from flask import render_template, flash, redirect, url_for, request
from shellmancer import app, db, bcrypt
from shellmancer.forms import RegisterForm, LoginForm, NewCampaignForm, UserSettingsForm
from shellmancer.models import UserAccount, SinglePlayerCampaign
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image


# Routes
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

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = UserAccount(email=form.email.data, password=hashed_pw)

        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.email.data}.", 'success')
        return redirect(url_for('login'))

    return render_template("register.html",
                           title="Register",
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('player_profile'))

    form = LoginForm()
    if form.validate_on_submit():

        user = UserAccount.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
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
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        current_user.agree_over_18 = form.agree_over_18.data
        db.session.commit()
        flash("Your account has been updated", 'success')
        return redirect(url_for('user_settings'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
        form.agree_over_18.data = current_user.agree_over_18
    return render_template('settings.html',
                           title=f"Settings for {current_user.email}",
                           form=form)



@app.route('/docs')
def docs():
    return render_template("docs.html")
