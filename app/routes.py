import email
from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt1, login_manager
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user


@app.route("/home")
def home():
    return render_template('home.html', title='home')

@app.route("/register", methods =['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt1.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created successfully. You are eligble to log in', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt1.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login Approved', 'success')
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', title='login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))