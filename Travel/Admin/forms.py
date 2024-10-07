from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateTimeField, IntegerField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


# create form for flight,hotel abd package
class FlightForm(FlaskForm):
    service_id = StringField('Service ID', validators=[DataRequired(), Length(max=50)],render_kw={"class": "form-control"})
    from1 = StringField('From', validators=[DataRequired(), Length(max=100)],render_kw={"class": "form-control"})
    to = StringField('To', validators=[DataRequired(), Length(max=100)],render_kw={"class": "form-control"})
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)],render_kw={"class": "form-control"})

    departure_time = DateTimeField('Departure Time', validators=[DataRequired()],format='%Y-%m-%dT%H:%M',render_kw={"class": "form-control","type": "datetime-local"})
    arrival_time = DateTimeField('Arrival Time', validators=[DataRequired()],format='%Y-%m-%dT%H:%M',render_kw={"class": "form-control","type": "datetime-local"})

    airline = StringField('Airline', validators=[DataRequired(), Length(max=100)],render_kw={"class": "form-control"})
    availability = BooleanField('Available', default=True)
    submit = SubmitField('Add Flight', 
                         render_kw={"class": "btn btn-primary"})

class HotelForm(FlaskForm):
    service_id = StringField('Service ID', validators=[DataRequired(), Length(max=50)],render_kw={"class": "form-control"})
    name = StringField('Name', validators=[DataRequired(), Length(max=50)],render_kw={"class": "form-control"})
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)],render_kw={"class": "form-control"})
    location = StringField('Location', validators=[DataRequired(), Length(max=100)],render_kw={"class": "form-control"})
    availability = BooleanField('Available', default=True)

class PackageDealForm(FlaskForm):
    flight_id = IntegerField('Flight ID', validators=[DataRequired()])
    hotel_id = IntegerField('Hotel ID', validators=[DataRequired()])
    availability = BooleanField('Available', default=True)
