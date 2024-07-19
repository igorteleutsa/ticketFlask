from app.models.role import Role
from app.models.status import Status
from app.models.permission import Permission
from app import db
from app.consts import (
    VIEW_USERS_PERMISSION, EDIT_USERS_PERMISSION, DELETE_USERS_PERMISSION,
    VIEW_GROUPS_PERMISSION, EDIT_GROUPS_PERMISSION, DELETE_GROUPS_PERMISSION,
    VIEW_TICKETS_PERMISSION, EDIT_TICKETS_PERMISSION, DELETE_TICKETS_PERMISSION
)


def initialize_defaults():
    default_roles = ['Admin', 'Manager', 'Analyst']
    for role in default_roles:
        if not Role.query.filter_by(name=role).first():
            db.session.add(Role(name=role))

    default_statuses = ['Pending', 'In review', 'Closed']
    for status in default_statuses:
        if not Status.query.filter_by(name=status).first():
            db.session.add(Status(name=status))

    default_permissions = [
        {'name': VIEW_USERS_PERMISSION, 'description': 'Can view users'},
        {'name': EDIT_USERS_PERMISSION, 'description': 'Can edit users'},
        {'name': DELETE_USERS_PERMISSION, 'description': 'Can delete users'},
        {'name': VIEW_GROUPS_PERMISSION, 'description': 'Can view groups'},
        {'name': EDIT_GROUPS_PERMISSION, 'description': 'Can edit groups'},
        {'name': DELETE_GROUPS_PERMISSION, 'description': 'Can delete groups'},
        {'name': VIEW_TICKETS_PERMISSION, 'description': 'Can view tickets'},
        {'name': EDIT_TICKETS_PERMISSION, 'description': 'Can edit tickets'},
        {'name': DELETE_TICKETS_PERMISSION, 'description': 'Can delete tickets'}
    ]

    for perm in default_permissions:
        if not Permission.query.filter_by(name=perm['name']).first():
            db.session.add(Permission(name=perm['name'], description=perm['description']))

    view_user_perm = Permission.query.filter_by(name=VIEW_USERS_PERMISSION).first()
    edit_user_perm = Permission.query.filter_by(name=EDIT_USERS_PERMISSION).first()
    delete_user_perm = Permission.query.filter_by(name=DELETE_USERS_PERMISSION).first()
    view_group_perm = Permission.query.filter_by(name=VIEW_GROUPS_PERMISSION).first()
    edit_group_perm = Permission.query.filter_by(name=EDIT_GROUPS_PERMISSION).first()
    delete_group_perm = Permission.query.filter_by(name=DELETE_GROUPS_PERMISSION).first()
    view_ticket_perm = Permission.query.filter_by(name=VIEW_TICKETS_PERMISSION).first()
    edit_ticket_perm = Permission.query.filter_by(name=EDIT_TICKETS_PERMISSION).first()
    delete_ticket_perm = Permission.query.filter_by(name=DELETE_TICKETS_PERMISSION).first()

    admin_role = Role.query.filter_by(name='Admin').first()
    manager_role = Role.query.filter_by(name='Manager').first()
    analyst_role = Role.query.filter_by(name='Analyst').first()

    admin_permissions = [
        view_user_perm, edit_user_perm, delete_user_perm,
        view_group_perm, edit_group_perm, delete_group_perm,
        view_ticket_perm, edit_ticket_perm, delete_ticket_perm
    ]

    manager_permissions = [
        view_user_perm, edit_user_perm, delete_user_perm,
        view_group_perm, edit_group_perm, delete_group_perm,
        view_ticket_perm, edit_ticket_perm, delete_ticket_perm
    ]

    analyst_permissions = [
        view_ticket_perm, edit_ticket_perm, delete_ticket_perm
    ]

    admin_role.permissions.extend(admin_permissions)
    manager_role.permissions.extend(manager_permissions)
    analyst_role.permissions.extend(analyst_permissions)

    db.session.commit()
