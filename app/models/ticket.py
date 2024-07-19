from app import db
from app.models.base import BaseModel


class Ticket(BaseModel):
    __tablename__ = 'ticket'
    name = db.Column(db.String(150), nullable=False)
    status_id = db.Column(db.String(36), db.ForeignKey('status.id'), nullable=False)
    note = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)
    group_id = db.Column(db.String(36), db.ForeignKey('group.id'), nullable=True)

    user = db.relationship('User', back_populates='tickets', overlaps="ticket_user", lazy=True)
    group = db.relationship('Group', back_populates='tickets', overlaps="ticket_group", lazy=True)
    status = db.relationship('Status', back_populates='tickets', overlaps="ticket_status", lazy=True)

    def __repr__(self) -> str:
        return f'<Ticket {self.name} - {self.status.name}>'
