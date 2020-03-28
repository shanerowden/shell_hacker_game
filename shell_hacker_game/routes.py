from flask import render_template, flash, redirect, url_for, request
from shell_hacker_game import app, db, bcrypt
from shell_hacker_game.forms import RegisterForm, LoginForm
from shell_hacker_game.models import UserAccount, PlayerProfile
from flask_login import login_user, current_user, logout_user, login_required


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

        flash(f"Account created for {form.email.data}. You are now able to login.", 'success')
        return redirect(url_for('login'))

    return render_template("register.html",
                           title="Register",
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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


@app.route('/docs')
def docs():
    return render_template("docs.html")
