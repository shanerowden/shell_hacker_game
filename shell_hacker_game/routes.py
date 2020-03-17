from flask import render_template, flash, redirect, url_for
from shell_hacker_game import app
from shell_hacker_game.forms import RegisterForm, LoginForm
from shell_hacker_game.models import UserAccount, PlayerProfile

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
