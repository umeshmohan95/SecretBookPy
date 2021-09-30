from flask import Blueprint,render_template,request,flash, redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_email = request.form.get('email')
        input_password = request.form.get('password')
        print(input_email,input_password)

        user = User.query.filter_by(email=input_email).first()
        if user:
            if check_password_hash(user.password, input_password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)   #remember the user histry and session
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Try again.', category='error')
        else:
            flash('Email does not exist.', category='error')


    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required         # make sure user login befrore logout
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist.', category='error')
        elif len(email) <4:
            flash('Email must be greater than 4 charecters.', category='error')
        elif len(first_name)< 2 :
            flash('First name must be greater than 2 charecters.', category='error')
        elif password1 != password2:
            flash('Password does not match', category='error')

        elif len(password1)< 7:
            flash('Password must be greater than 7 charecters.', category='error')

        else:

            new_user = User(email=email, first_name=first_name, password= generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user = current_user)