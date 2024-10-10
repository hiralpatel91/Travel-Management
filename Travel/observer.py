
from Travel import app,mail
from flask_mail import Message

# create observer
class Observer:
    def update(self, message,sender):
        pass

# class for notify user
class EmailNotifier(Observer):
    def __init__(self, recipient_email):
        self.recipient_email = recipient_email

    def update(self, message,sender):
        msg = Message("Booking Notification", recipients=[self.recipient_email],sender=sender)
        msg.body = message
        with app.app_context():
            mail.send(msg)

class BookingSubject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, message,sender):
        for observer in self.observers:
            observer.update(message,sender)
