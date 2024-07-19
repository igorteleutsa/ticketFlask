from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.controllers.user_controller import register_user, authenticate_user, get_all_roles, get_all_groups

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_id = request.form['role_id']
        group_ids = request.form.getlist('group_ids')

        user = register_user(username, email, password, role_id, group_ids)
        if user:
            flash('Your account has been created!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email already registered. Please choose a different email or login.', 'danger')
            return redirect(url_for('auth.register'))

    roles = get_all_roles()
    groups = get_all_groups()
    return render_template('register.html', roles=roles, groups=groups)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = authenticate_user(email, password)
        if user:
            login_user(user)
            return redirect(url_for('home.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
