from flask_sqlalchemy import SQLAlchemy

db =SQLAlchemy()
class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    name_en = db.Column(db.String(20), nullable=False)