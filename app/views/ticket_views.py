from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app.consts import VIEW_TICKETS_PERMISSION, EDIT_TICKETS_PERMISSION, DELETE_TICKETS_PERMISSION
from app.controllers.ticket_controller import (
    get_all_tickets, get_tickets_for_user, create_ticket, get_ticket_by_id, update_ticket, delete_ticket,
    get_all_statuses, get_all_users, get_all_groups
)
from app.decorators import permission_required

ticket_blueprint = Blueprint('ticket', __name__)


@ticket_blueprint.route('/tickets')
@login_required
@permission_required(VIEW_TICKETS_PERMISSION)
def tickets():
    if current_user.has_role('Admin'):
        tickets = get_all_tickets()
    else:
        tickets = get_tickets_for_user(current_user)
    return render_template('tickets.html', tickets=tickets)


@ticket_blueprint.route('/ticket/add', methods=['GET', 'POST'])
@permission_required(EDIT_TICKETS_PERMISSION)
def add_ticket():
    if request.method == 'POST':
        success, error = create_ticket(request.form)
        if not success:
            return error, 400
        return redirect(url_for('ticket.tickets'))

    statuses = get_all_statuses()
    users = get_all_users()
    groups = get_all_groups()
    return render_template('add_ticket.html', statuses=statuses, users=users, groups=groups)


@ticket_blueprint.route('/ticket/edit/<ticket_id>', methods=['GET', 'POST'])
@permission_required(EDIT_TICKETS_PERMISSION)
def edit_ticket(ticket_id):
    if request.method == 'POST':
        success, error = update_ticket(ticket_id, request.form)
        if not success:
            return error, 400
        return redirect(url_for('ticket.tickets'))

    ticket = get_ticket_by_id(ticket_id)
    statuses = get_all_statuses()
    users = get_all_users()
    groups = get_all_groups()
    return render_template('edit_ticket.html', ticket=ticket, statuses=statuses, users=users, groups=groups)


@ticket_blueprint.route('/ticket/<ticket_id>')
@login_required
@permission_required(VIEW_TICKETS_PERMISSION)
def ticket_detail(ticket_id):
    ticket = get_ticket_by_id(ticket_id)
    return render_template('ticket_detail.html', ticket=ticket)


@ticket_blueprint.route('/ticket/delete/<ticket_id>', methods=['POST'])
@permission_required(DELETE_TICKETS_PERMISSION)
def delete_ticket_view(ticket_id):
    delete_ticket(ticket_id)
    return redirect(url_for('ticket.tickets'))
