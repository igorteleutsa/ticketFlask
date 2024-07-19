import pytest
from app import create_app, db
from app.models.user import User
from app.models.role import Role
from app.models.group import Group
from app.models.status import Status
from app.models.ticket import Ticket
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            initialize_database()
        yield testing_client

    with app.app_context():
        db.drop_all()


def initialize_database():
    if not Role.query.first():
        admin_role = Role(name='Admin')
        manager_role = Role(name='Manager')
        analyst_role = Role(name='Analyst')
        db.session.add_all([admin_role, manager_role, analyst_role])
        db.session.commit()

    if not Group.query.first():
        group1 = Group(name='Group 1')
        group2 = Group(name='Group 2')
        db.session.add_all([group1, group2])
        db.session.commit()

    if not Status.query.first():
        pending_status = Status(name='Pending')
        in_review_status = Status(name='In review')
        closed_status = Status(name='Closed')
        db.session.add_all([pending_status, in_review_status, closed_status])
        db.session.commit()

    if not User.query.filter_by(email='admin@example.com').first():
        admin_role = Role.query.filter_by(name='Admin').first()
        manager_role = Role.query.filter_by(name='Manager').first()
        analyst_role = Role.query.filter_by(name='Analyst').first()
        group1 = Group.query.filter_by(name='Group 1').first()
        group2 = Group.query.filter_by(name='Group 2').first()

        admin_user = User(username='admin', email='admin@example.com', password=generate_password_hash('password'),
                          role=admin_role)
        manager_user = User(username='manager', email='manager@example.com',
                            password=generate_password_hash('password'), role=manager_role)
        analyst_user1 = User(username='analyst1', email='analyst1@example.com',
                             password=generate_password_hash('password'), role=analyst_role, groups=[group1])
        analyst_user2 = User(username='analyst2', email='analyst2@example.com',
                             password=generate_password_hash('password'), role=analyst_role, groups=[group2])
        db.session.add_all([admin_user, manager_user, analyst_user1, analyst_user2])
        db.session.commit()

    if not Ticket.query.first():
        pending_status = Status.query.filter_by(name='Pending').first()
        group1 = Group.query.filter_by(name='Group 1').first()
        group2 = Group.query.filter_by(name='Group 2').first()

        ticket1 = Ticket(name='Ticket 1', status=pending_status, group=group1)
        ticket2 = Ticket(name='Ticket 2', status=pending_status, group=group2)
        db.session.add_all([ticket1, ticket2])
        db.session.commit()
