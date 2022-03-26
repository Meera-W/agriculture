from agritech import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    username = db.Column(db.String(200),nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    equipments = db.relationship('Equipment',backref='owner',lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eqname = db.Column(db.String(200),nullable=False)
    location = db.Column(db.String(200),nullable=False)
    price = db.Column(db.String(200),nullable=False)
    contact = db.Column(db.String(200),nullable=False)
    filename = db.Column(db.String(200),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.eqname}', '{self.qty}')"