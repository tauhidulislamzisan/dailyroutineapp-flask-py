from app import app

from app import routes
from app import User
from app import db

def create_default_user():
    with app.app_context():
        db.create_all()
@app.before_first_request
def initialize_app():
    create_default_user()
    
if __name__ == "__main__":
    app.run(debug=True)