# In Python console or script
from index import create_app, db
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()