from flask import Flask
from index.views import main_bp  
from index import create_app  # Ensure this imports the create_app function from your __init__.py

app = create_app()  # Create the Flask app using the create_app function

if __name__ == "__main__":
    try:
        app.run(debug=True)  # Start the Flask development server
    except Exception as e:
        print(f"Error running app: {e}")
