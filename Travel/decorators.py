from functools import wraps
from flask import session, redirect, url_for,request
import logging

# Decorator to check admin login
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_id'):
            return redirect(url_for('adminlogin'))
        return f(*args, **kwargs)
    return decorated_function

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Decorator for booking
def log_booking_attempt(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            result=func(*args,**kwargs)
            logging.info(f"Reservation Successsful:{kwargs}")
            return result
        except Exception as e:
            logging.error(f"Booking failed: {e}, args: {args}, kwargs: {kwargs}")
            raise
    return wrapper

# decorator for validate booking details
def validate_booking_details(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        reservation_data = request.form
        
        optional_fields = ['package_deal_id', 'flight_id', 'hotel_id']

        # Ensure at least one of the optional fields is provided
        if not any(reservation_data.get(field) for field in optional_fields):
            raise ValueError("At least one of package_deal_id, flight_id, or hotel_id must be provided.")


        return func(reservation_data, *args, **kwargs)
    return wrapper

