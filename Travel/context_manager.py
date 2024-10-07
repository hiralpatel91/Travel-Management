from contextlib import contextmanager
from flask import current_app
from Travel import db


# Context manager for handling booking sessions.
@contextmanager
def BookingContext():
    
    session = db.session

    # Reservation is begin
    if not session.is_active:
        session.begin_nested()  

    try:
        yield session  # Yield the session to the caller
    except Exception as e:
        # Roll back the session on error
        session.rollback()
        current_app.logger.error(f"Booking failed: {e}")
        raise  # Re-raise the exception after rollback
    else:
        session.commit()
    finally:
        if not session.is_active:
            session.remove() 
