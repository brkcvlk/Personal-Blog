from flask import Blueprint, request, render_template, flash, redirect, url_for
from .models import User
from flask_login import login_user, login_required, logout_user


auth = Blueprint('auth', __name__)

admin = User(username = 'Admin',password= 'Admin')
guest = User(username = 'Guest',password= 'Guest')


@auth.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        if request.form:
            username = request.form.get('name')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    flash(f'Welcome {user.username} !', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.Admin'))
                else:
                    flash('Passwords dont match', category='error')
            else:
                flash(f'There is no user about with {user}', category='error')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('auth.Login'))