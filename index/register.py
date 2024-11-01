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
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate that no field is missing
        if not all([first_name, last_name, dob, email, username, password]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Store the user data in the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (first_name, last_name, dob, email, username, password) VALUES (?, ?, ?, ?, ?, ?)',
                      (first_name, last_name, dob, email, username, hashed_password))
            conn.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'danger')
        finally:
            conn.close()

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
