from app import db
from app.models.base import BaseModel


class Status(BaseModel):
    __tablename__ = 'status'
    name = db.Column(db.String(50), unique=True, nullable=False)
    tickets = db.relationship('Ticket', back_populates='status', overlaps="ticket_status", lazy=True)

    def __repr__(self) -> str:
        return f'<Status {self.name}>'
