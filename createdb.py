from index import create_app, db
from index.models import User

app = create_app()

with app.app_context():
    db.create_all()
