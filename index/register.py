import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a more secure secret key

# Function to initialize the SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')
    conn.commit()
    conn.close()

# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        contact_number = request.form['contact_number']
        street_address = request.form['street_address']

        # Create database connection
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Create users table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            street_address TEXT NOT NULL
        )''')

        try:
            # Check if username already exists
            c.execute('SELECT username FROM users WHERE username = ?', (username,))
            if c.fetchone():
                flash('Username already exists! Please choose a different username.', 'danger')
                return redirect(url_for('main.register'))

            # Check if email already exists
            c.execute('SELECT email FROM users WHERE email = ?', (email,))
            if c.fetchone():
                flash('Email already registered! Please use a different email.', 'danger')
                return redirect(url_for('main.register'))

            # Hash the password
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            # Insert new user
            c.execute('''INSERT INTO users 
                (first_name, last_name, dob, email, username, password, contact_number, street_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (first_name, last_name, dob, email, username, hashed_password, contact_number, street_address))
            
            # Commit the transaction
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('dashboard'))

        except sqlite3.IntegrityError as e:
            flash('An error occurred during registration. Please try again.', 'danger')
            print(f"Database error: {e}")  # For debugging
            return redirect(url_for('main.register'))

        except Exception as e:
            flash('An unexpected error occurred. Please try again.', 'danger')
            print(f"Unexpected error: {e}")  # For debugging
            return redirect(url_for('main.register'))

        finally:
            # Always close the connection
            conn.close()

    # GET request - show registration form
    return render_template('register.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()  # Get user data
        conn.close()

        if user and check_password_hash(user[6], password):  # Adjust the index based on your table structure
            session['user_id'] = user[0]  # Store user ID in the session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to a dashboard or home page
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')

# Route for the dashboard (protected)
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return 'Welcome to your dashboard!'
    return redirect(url_for('login'))

# Run the application
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
