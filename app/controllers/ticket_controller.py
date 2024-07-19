from app.models.group import Group
from app.models.ticket import Ticket
from app.models.status import Status
from app.models.user import User
from app import db
from typing import Optional


def get_all_tickets() -> list[Ticket]:
    return Ticket.query.all()


def get_all_groups() -> list[Group]:
    return Group.query.all()


def get_all_statuses() -> list[Status]:
    return Status.query.all()


def get_all_users() -> list[User]:
    return User.query.all()


def get_tickets_for_user(user) -> list[Ticket]:
    tickets = Ticket.query.filter((Ticket.user_id == user.id) |
                                  (Ticket.group_id.in_([group.id for group in user.groups]))).all()
    return tickets


def get_ticket_by_id(ticket_id: str) -> Ticket:
    return db.session.get(Ticket, ticket_id)


def create_ticket(data: dict) -> tuple[bool, Optional[str]]:
    name = data.get('name')
    status_id = data.get('status_id')
    note = data.get('note')
    group_id = data.get('group_id') if data.get('group_id') != 'None' else None
    user_id = data.get('user_id') if data.get('user_id') != 'None' else None

    if not name or not status_id or not group_id:
        return False, "Missing required fields"

    try:
        ticket = Ticket(
            name=name,
            status_id=status_id,
            note=note,
            group_id=group_id,
            user_id=user_id
        )
        db.session.add(ticket)
        db.session.commit()
        return True, None
    except Exception as e:
        return False, str(e)


def update_ticket(ticket_id: str, data: dict) -> tuple[bool, Optional[str]]:
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        return False, "Ticket not found"
    name = data.get('name')
    status_id = data.get('status_id')
    note = data.get('note')
    group_id = data.get('group_id') if data.get('group_id') != 'None' else None
    user_id = data.get('user_id') if data.get('user_id') != 'None' else None

    if not name or not status_id or not group_id:
        return False, "Missing required fields"

    try:
        ticket.name = name
        ticket.status_id = status_id
        ticket.note = note
        ticket.group_id = group_id
        ticket.user_id = user_id
        db.session.commit()
        return True, None
    except Exception as e:
        return False, str(e)


def delete_ticket(ticket_id: str) -> None:
    ticket = get_ticket_by_id(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
