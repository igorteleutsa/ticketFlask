from app.database import db

from app.models.base import BaseModel

# Association table for many-to-many relationship between users and groups
user_groups = db.Table('user_groups',
    db.Column('user_id', db.String(36), db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.String(36), db.ForeignKey('group.id'), primary_key=True)
)


class Group(BaseModel):
    __tablename__ = 'group'
    name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_groups, back_populates='groups', lazy='subquery')
    tickets = db.relationship('Ticket', back_populates='group', overlaps="ticket_group", lazy=True)

    def __repr__(self) -> str:
        return f'<Group {self.name}>'
