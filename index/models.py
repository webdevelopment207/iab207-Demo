from flask_login import UserMixin  # Import UserMixin for Flask-Login
from index import db
from datetime import datetime


class User(UserMixin, db.Model):  # Inherit from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # For storing hashed passwords

    def __repr__(self):
        return f'<User {self.username}>'
     # Method to get initials from the user's first and last name
    def get_initials(self):
        return f"{self.first_name[0].upper()}{self.last_name[0].upper()}"


class Event(db.Model):
    __tablename__ = 'events'  # Ensure this matches your database table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=True)
    seats_available = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Open')
    price_per_ticket = db.Column(db.Float, nullable=False)  # Add this line for price per ticket
    comments = db.relationship('Comment', backref='event', lazy=True)
    tickets = db.relationship('Ticket', back_populates='event', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.id} - {self.name}, Status: {self.status}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Assuming the User model is already created
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)  # Add ForeignKey constraint here
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    
class Ticket(db.Model):
    __tablename__ = 'tickets'  # Ensure this matches your database table name
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)  # Add this line for total price
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)  # Add this line
    event = db.relationship('Event', back_populates='tickets')

    def __repr__(self):
        return f'<Ticket {self.id} - {self.user_name}, Event ID: {self.event_id}>'