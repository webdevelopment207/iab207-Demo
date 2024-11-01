# RealTickets - Event Ticketing System

A Flask-based event ticketing system designed for sports events, built as part of IAB207 at QUT.

## Features

- 🎫 Event Creation and Management
- 👤 User Authentication and Profiles
- 🛒 Ticket Booking System
- 💬 Event Comments and Reviews
- 📱 Responsive Design
- 🔒 Secure User Authentication
- 📊 Booking History Tracking

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5, Custom CSS
- **Security**: Werkzeug Security

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/realtickets.git
cd realtickets
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```python
>>> from index import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

5. Run the application:
```bash
python main.py
```

## Configuration

Create a `.env` file in the root directory with the following variables:
```env
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///users.db
```

## Project Structure

```
realtickets/
├── index/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── static/
│   └── templates/
├── main.py
├── createdb.py
├── populate_db.py
├── requirements.txt
└── README.md
```

## Usage

### Running the Application
After installation, run:
```bash
python main.py
```
Navigate to `http://localhost:5000` in your web browser.

### Creating an Account
1. Click "Register" in the navigation bar
2. Fill in your details
3. Submit the registration form
4. Log in with your credentials

### Creating an Event
1. Log in to your account
2. Click "Create Event" in the navigation
3. Fill in the event details
4. Upload an event image (optional)
5. Submit the form

### Booking Tickets
1. Browse available events on the home page
2. Click on an event to view details
3. Click "Book Tickets"
4. Select the number of tickets
5. Complete the booking form
6. Confirm your booking

## Development

### Setting Up Development Environment

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies:
```bash
pip install -r requirements.txt
```