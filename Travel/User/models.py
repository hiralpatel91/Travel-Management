from flask_login import UserMixin
from Travel import db,login_manager
from datetime import datetime
from Travel.Admin.models import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(128), unique=False)

    

    def __repr__(self):
        return '<User %r>' % self.username
    
# user reservation model
class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Assuming you have an Admin model for users
    package_deal_id = db.Column(db.Integer, db.ForeignKey('package_deals.id'), nullable=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=True)
    reservation_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(50), default='Confirmed')  # Adding status field
    package_deal = db.relationship('PackageDeal', backref='reservations')
    flight = db.relationship('Flight', backref='reservations')
    hotel = db.relationship('Hotel', backref='reservations')
    user = db.relationship('User', backref='reservations')

    def __repr__(self):
        return f"<Reservation {self.id}>"

    
db.create_all()

