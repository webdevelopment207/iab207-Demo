import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from index import db  # Import the db instance from your app file
from index.models import User, Comment, Event, Ticket  # Import models in one line for clarity
from flask_login import logout_user, login_required, current_user, login_user
from datetime import datetime  # Import datetime for date handling

# Define the Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    events = Event.query.all()
    print(events)  # Debug line
    return render_template('homepage.html', events=events)

# Registration route
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists! Please choose a different username.', 'danger')
            return redirect(url_for('main.register'))

        # Hash the password and save the new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(first_name=first_name, last_name=last_name, dob=dob, email=email, username=username, password=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

# Login route
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('User not found. Please register first.', 'danger')
            return redirect(url_for('main.register'))

        # Verify the password
        if not check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('main.login'))

        # Log the user in
        login_user(user)

        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('main.home'))

    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('main.login'))

@main_bp.route('/event/<int:event_id>/comment', methods=['POST'])
@login_required
def post_comment(event_id):
    content = request.form.get('content')
    if content:
        new_comment = Comment(content=content, user_id=current_user.id, event_id=event_id)
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment posted successfully!", "success")
    else:
        flash("Comment cannot be empty.", "danger")
    return redirect(url_for('main.event_details', event_id=event_id))

@main_bp.route('/event/<int:event_id>')
def event_details(event_id):
    event = Event.query.get(event_id)
    if event is None:
        flash('Event not found', 'danger')
        return redirect(url_for('main.home'))

    return render_template('event_details.html', event=event)

@main_bp.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        home_team = request.form.get('homeTeam')
        away_team = request.form.get('awayTeam')
        venue = request.form.get('venue')
        event_date = request.form.get('eventDate')
        event_time = request.form.get('eventTime')
        description = request.form.get('eventDescription')
        seats_available = request.form.get('seatsAvailable')
        status = request.form.get('status')
        price_per_ticket = request.form.get('price_per_ticket')  # Ensure this is included
        event_image = request.files.get('eventImage')  # Get the uploaded file

        # Debug output
        print(f"Received price_per_ticket: {price_per_ticket}")  # Check what is being received

        # Check if price_per_ticket is not None or empty
        if price_per_ticket is None or price_per_ticket.strip() == '':
            flash('Please provide a price for the ticket.', 'danger')
            return redirect(url_for('main.create_event'))

        try:
            price_per_ticket = float(price_per_ticket)  # Convert to float
        except ValueError:
            flash('Invalid price format. Please enter a valid number.', 'danger')
            return redirect(url_for('main.create_event'))

        # Combine event_date and event_time into a single datetime string
        date_str = f"{event_date} {event_time}"
        try:
            event_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        except ValueError as e:
            flash(f"Date and time format is incorrect: {e}", "danger")
            return redirect(url_for('main.create_event'))

        # Handle image upload
        if event_image:
            filename = event_image.filename
            # Save the image to the upload folder
            image_path = os.path.join('path/to/upload/folder', filename)  # Update with your actual upload path
            event_image.save(image_path)
            # Save the image filename to the event object
            image_filename = filename
        else:
            image_filename = None  # Handle case where no image is uploaded

        # Create a new event object with the image filename
        new_event = Event(
            name=f"{home_team} vs {away_team}",
            location=venue,
            date=event_datetime,
            description=description,
            seats_available=int(seats_available),
            status=status,
            price_per_ticket=price_per_ticket,  # Save the price to the database
            image_filename=image_filename  # Add this line to save the image filename
        )

        db.session.add(new_event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for('main.home'))

    return render_template('create_event.html')

# Error handling routes
@main_bp.route('/404')
def page_not_found():
    return render_template('error.html', error_code=404), 404

@main_bp.route('/500')
def server_error():
    return render_template('error.html', error_code=500), 500

@main_bp.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404), 404

@main_bp.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500), 500

@main_bp.route('/tickets/<int:event_id>', methods=['GET', 'POST'])
def tickets(event_id):
    event = Event.query.get_or_404(event_id)

    if not current_user.is_authenticated:
        flash('Unable to fulfil request, please log in first.', 'danger')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        number_of_tickets = request.form.get('numberOfTickets', type=int)
      # Check for existing ticket
        existing_ticket = Ticket.query.filter_by(
            event_id=event.id,
            user_name=request.form['name'],
            user_email=request.form['email']
        ).first()
        if existing_ticket:
            flash('You have already booked tickets for this event.', 'danger')
            return redirect(url_for('main.tickets', event_id=event_id))

        # Check if the number of tickets exceeds the limit (10)
        if number_of_tickets > 10:
            flash('You cannot book more than 10 tickets at a time. Please reduce the number of tickets.', 'danger')
            return redirect(url_for('main.tickets', event_id=event_id))

        # Check if there are enough seats available
        if number_of_tickets > event.seats_available:
            flash('Not enough seats available for your request. Please reduce the number of tickets.', 'danger')
            return redirect(url_for('main.tickets', event_id=event_id))

        # Calculate the total price
        total_price = event.price_per_ticket * number_of_tickets

        # If validation passes, create a ticket and reduce available seats
        ticket = Ticket(
            event_id=event.id,
            user_name=request.form['name'],
            user_email=request.form['email'],
            number_of_tickets=number_of_tickets,
            total_price=total_price
        )
        db.session.add(ticket)
        event.seats_available -= number_of_tickets  # Reduce the number of available seats
        db.session.commit()

        # Only flash the success message once, after the ticket is saved
        flash('Tickets booked successfully!', 'success')
        return redirect(url_for('main.tickets', event_id=event_id))

    return render_template('tickets.html', event=event)


@main_bp.route('/booking-history')
@login_required  # Ensure user is logged in to access booking history
def booking_history():
    # Query tickets for the current user
    bookings = Ticket.query.filter_by(user_email=current_user.email).all()
    
    return render_template('booking_history.html', bookings=bookings)

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Logic to update user profile
        username = request.form['username']
        email = request.form['email']
        bio = request.form['bio']
        
        # Update the current user's information
        current_user.username = username
        current_user.email = email
        current_user.bio = bio
        
        # Commit changes to the database
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    return render_template('profile.html')

@main_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    username = request.form['username']
    email = request.form['email']
    bio = request.form['bio']

    # Update the current user's information
    current_user.username = username
    current_user.email = email
    current_user.bio = bio

    # Commit changes to the database
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('main.profile'))