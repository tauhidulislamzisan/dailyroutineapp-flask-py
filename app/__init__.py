from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "the_secret_keeper"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://root:password@localhost/routine'
        )
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please Login First"
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(125), nullable=False)
    email = db.Column(db.String(125), nullable=False)
    password = db.Column(db.String(125), nullable=False)
    is_admin = db.Column(db.Boolean, default=0)
    routine = db.relationship("Routine", backref="user")

class Routine(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    details = db.Column(db.Text)
    done = db.Column(db.Boolean, default=0)
    update_time = db.Column(db.DateTime,default=datetime.now)
    created_time = db.Column(db.DateTime,default=datetime.now)



