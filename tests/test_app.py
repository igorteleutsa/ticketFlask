import pytest
from flask import url_for
from app.models.user import User
from app.models.ticket import Ticket
from app.models.status import Status
from app.models.group import Group
from app import db


def login(client, email, password):
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_register_user(test_client):
    response = test_client.post('/register', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='password',
        role_id='1'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_logout(test_client):
    response = login(test_client, 'admin@example.com', 'password')
    assert response.status_code == 200
    assert b'Logout' in response.data

    response = logout(test_client)
    assert response.status_code == 200
    assert b'Login' in response.data


def test_create_ticket(test_client):
    login(test_client, 'admin@example.com', 'password')

    status = Status.query.filter_by(name='Pending').first()
    group = Group.query.filter_by(name='Group 1').first()

    print(f"Status ID: {status.id}")
    print(f"Group ID: {group.id}")

    response = test_client.post('/ticket/add', data=dict(
        name='Test Ticket',
        status_id=str(status.id),
        note='This is a test ticket.',
        group_id=str(group.id)
    ), follow_redirects=True)

    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.data.decode('utf-8')}")
    assert response.status_code == 200
    assert b'Test Ticket' in response.data


def test_edit_ticket(test_client):
    login(test_client, 'admin@example.com', 'password')
    ticket = Ticket.query.filter_by(name='Ticket 1').first()

    status = Status.query.filter_by(name='In review').first()

    response = test_client.post(f'/ticket/edit/{ticket.id}', data=dict(
        name='Updated Ticket',
        status_id=str(status.id),
        note='This is an updated test ticket.',
        group_id=str(ticket.group_id)
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Updated Ticket' in response.data


def test_delete_ticket(test_client):
    login(test_client, 'admin@example.com', 'password')
    ticket = Ticket.query.filter_by(name='Ticket 2').first()
    response = test_client.post(f'/ticket/delete/{ticket.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Ticket 2' not in response.data
