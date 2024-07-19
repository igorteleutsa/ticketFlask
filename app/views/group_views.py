from flask import Blueprint, render_template, request, redirect, url_for

from app.consts import VIEW_GROUPS_PERMISSION, EDIT_GROUPS_PERMISSION
from app.controllers.group_controller import get_all_groups, create_group, get_group_by_id
from app.decorators import permission_required

group_blueprint = Blueprint('group', __name__)


@group_blueprint.route('/groups')
@permission_required(VIEW_GROUPS_PERMISSION)
def groups():
    groups = get_all_groups()
    return render_template('groups.html', groups=groups)


@group_blueprint.route('/group/add', methods=['GET', 'POST'])
@permission_required(EDIT_GROUPS_PERMISSION)
def add_group():
    if request.method == 'POST':
        name = request.form['name']
        create_group(name)
        return redirect(url_for('group.groups'))
    return render_template('add_group.html')


@group_blueprint.route('/group/<group_id>')
@permission_required(VIEW_GROUPS_PERMISSION)
def group_detail(group_id):
    group = get_group_by_id(group_id)
    return render_template('group_detail.html', group=group)
