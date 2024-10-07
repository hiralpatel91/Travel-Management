from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:root@localhost/travel'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@localhost/travel'

app.config["SECRET_KEY"] = "380809898a208a9402023cb802ddede5"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
migrate = Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'
login_manager.needs_refresh_message_category='danger'
# login_manager.login_message = u'Please Login First'

# Email authentication to notify the user
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hiraltalaviya8@gmail.com'  
app.config['MAIL_PASSWORD'] = 'bkxt ifeb nyvk cknq'  


mail = Mail(app)

from Travel.Admin.models import *
from Travel.User.models import *




# register blue print
def create_app():
    from Travel.Admin.routes import bp
    app.register_blueprint(bp)
    from Travel.User.routes import bp
    app.register_blueprint(bp)
    return app

with app.app_context():
    # Import your models here to avoid circular imports
    from Travel.User.models import Flight, Hotel, TravelService
    
    # Query existing flights and hotels from the database
    existing_flights = Flight.query.all()
    existing_hotels = Hotel.query.all()
    
    # Register each flight in the service registry
    for flight in existing_flights:
        TravelService._service_registry.append(flight)

    # Register each hotel in the service registry
    for hotel in existing_hotels:
        TravelService._service_registry.append(hotel)