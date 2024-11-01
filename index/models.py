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
    bio = db.Column(db.Text, nullable=True)  # Optional field for user bio
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Track creation time

    def __repr__(self):
        return f'<User {self.username}>'

    # Method to get initials from the user's first and last name
    def get_initials(self):
        return f"{self.first_name[0].upper()}{self.last_name[0].upper()}"

    # Method to update password
    def set_password(self, new_password):
        self.password = generate_password_hash(new_password, method='pbkdf2:sha256')


class Event(db.Model):
    __tablename__ = 'events'  # Ensure this matches your database table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=True)
    seats_available = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Open')  # Default to 'Open'
    price_per_ticket = db.Column(db.Float, nullable=False)  # Price per ticket
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Reference to the user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Track creation time
    comments = db.relationship('Comment', backref='event', lazy=True)
    tickets = db.relationship('Ticket', back_populates='event', cascade='all, delete-orphan')
    image_filename = db.Column(db.String(120), nullable=True)  # Image filename

    def __repr__(self):
        return f'<Event {self.id} - {self.name}, Status: {self.status}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)  # Foreign key to Event
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for comment
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comment {self.id} by User {self.user_id}>'


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='confirmed')  # Status of the ticket
    event = db.relationship('Event', back_populates='tickets')

    def __repr__(self):
        return f'<Ticket {self.id} - {self.user_name}, Event ID: {self.event_id}>'
    
    @property
    def formatted_id(self):
        # Format the ID as ORD-0001, ORD-0002, etc.
        return f'ORD-{self.id:04d}'
