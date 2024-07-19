from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.consts import VIEW_USERS_PERMISSION, EDIT_USERS_PERMISSION, DELETE_USERS_PERMISSION
from app.controllers.user_controller import (
    get_all_users, create_user, get_user_by_id, update_user, delete_user,
    get_all_roles, get_all_groups, check_email_exists
)
from app.decorators import permission_required

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/users')
@login_required
@permission_required(VIEW_USERS_PERMISSION)
def users():
    users = get_all_users()
    return render_template('users.html', users=users)


@user_blueprint.route('/user/add', methods=['GET', 'POST'])
@permission_required(EDIT_USERS_PERMISSION)
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_id = request.form['role_id']
        group_ids = request.form.getlist('group_ids')

        if check_email_exists(email):
            flash('Email already registered. Please choose a different email.', 'danger')
            return redirect(url_for('user.add_user'))

        create_user(username, email, password, role_id, group_ids)
        return redirect(url_for('user.users'))

    roles = get_all_roles()
    groups = get_all_groups()
    return render_template('add_user.html', roles=roles, groups=groups)


@user_blueprint.route('/user/<user_id>')
@login_required
@permission_required(VIEW_USERS_PERMISSION)
def user_detail(user_id):
    user = get_user_by_id(user_id)
    return render_template('user_detail.html', user=user)


@user_blueprint.route('/user/edit/<user_id>', methods=['GET', 'POST'])
@permission_required(EDIT_USERS_PERMISSION)
def edit_user(user_id):
    user = get_user_by_id(user_id)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role_id = request.form['role_id']
        group_ids = request.form.getlist('group_ids')

        if check_email_exists(email) and email != user.email:
            flash('Email already registered. Please choose a different email.', 'danger')
            return redirect(url_for('user.edit_user', user_id=user_id))

        update_user(user_id, username, email, role_id, group_ids)
        return redirect(url_for('user.user_detail', user_id=user_id))

    roles = get_all_roles()
    groups = get_all_groups()
    return render_template('edit_user.html', user=user, roles=roles, groups=groups)


@user_blueprint.route('/user/delete/<user_id>', methods=['POST'])
@permission_required(DELETE_USERS_PERMISSION)
def delete_user_view(user_id):
    delete_user(user_id)
    return redirect(url_for('user.users'))
