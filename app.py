from flask import (
    Flask, render_template, flash, redirect, url_for
)
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm

import os

app = Flask("shell_hacker_game")
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import UserAccount, PlayerProfile

# Routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.email.data}", 'purple')
        return redirect(url_for('home'))
    return render_template("register.html",
                           title="Register",
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f"You have been logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template("login.html",
                           title="Login",
                           form=form)
