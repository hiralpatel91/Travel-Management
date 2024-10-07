from flask import render_template,Blueprint,request,redirect,url_for,flash,jsonify,session
from Travel import app,db,bcrypt
from Travel.User.models import User,Reservation
from Travel.User.forms import UserSigninForm, UserSignUpForm, UserProfileUpdateForm
from flask_login import login_user,logout_user,login_required,current_user
from Travel.Admin.models import Flight,Hotel,PackageDeal
from Travel.context_manager import BookingContext
from Travel.decorators import log_booking_attempt, validate_booking_details
from Travel.metaclasses import ServiceMeta
from Travel.observer import BookingSubject, EmailNotifier




bp = Blueprint("user",__name__)


@app.route('/')
def home():
    return render_template('user/index.html',title="User")



# _____________________Authentication__________________________

# signup
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserSignUpForm()
    
    if request.method == 'POST':
        # Validate the form
        if form.validate_on_submit():
            # Hash the password and create a new user
            hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hash_password)
            db.session.add(user)
            db.session.commit()
            flash("Registered Successfully", 'success')
            return redirect('signin')
        
        # If the form is invalid, log the errors and flash a message
        flash("Registration unsuccessful. Please check your inputs.", 'danger')
        return render_template("user/register.html", form=form,title="User Signup")  

    return render_template("user/register.html", form=form,title="User Signup")

# signin
@app.route('/signin',methods=['GET','POST'])
def signin():
    form = UserSigninForm(request.form)

    if 'login_message_shown' not in session:
            flash('Please Login First', 'danger')
            session['login_message_shown'] = True

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            session['user_id'] = user.id  
            session['user_email'] = user.email
            flash('You are login now!','success')
            # set a cookies for user
            response = redirect(url_for('home'))
            response.set_cookie('user_email', user.email, max_age=60*60*24*30)  # Cookie lasts 30 days
            return response
        
            
        flash("Invalid username and password",'danger')
        return redirect('signin')
    session.pop('login_message_shown', None)  # Reset the flag for the next visit
    return render_template('user/login.html',form=form,title="User Signin")

# logout user
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('signin')


# UPdate user profile And Password
@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    user = User.query.get(user_id)
    form = UserProfileUpdateForm(obj=user)

    if form.validate_on_submit():
        # Check current password only if a new password is being set
        if form.new_password.data and not bcrypt.check_password_hash(user.password, form.current_password.data):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('update_user', user_id=user.id))

        # Update username and email
        user.username = form.username.data
        user.email = form.email.data

        # Update password if a new one is provided
        if form.new_password.data:
            user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            logout_user()

        # Commit changes to the database
        db.session.commit()
        flash('Account updated successfully', 'success')
        return redirect(url_for('user_dashboard', user_id=user.id))
    else:
        print(form.errors)  # Debugging output for validation errors

    return render_template('user/update_account.html', form=form)

# ______________________Authentication ends_______________________________________


# ___________________________Reservation ____________________________________

@app.route('/book', methods=['GET', 'POST'])
@login_required
@log_booking_attempt
@validate_booking_details
def book(reservation_data=None):
    if request.method == 'POST':
        user_id = current_user.id
        
        package_deal_id = request.form.get('package_deal_id')
        flight_id = request.form.get('flight_id')
        hotel_id = request.form.get('hotel_id')

        # Ensure the user is authenticated
        if not current_user.is_authenticated:
            return jsonify({"error": "User not authenticated"}), 403

        # Check for existing reservations
        existing_reservation = Reservation.query.filter_by(
            user_id=user_id,
            package_deal_id=package_deal_id,
            flight_id=flight_id,
            hotel_id=hotel_id,
            status="Confirmed"
        ).first()

        if existing_reservation:
            flash("You have already booked this reservation.", 'warning')
            return redirect(url_for('user_dashboard', user_id=user_id))

        # Retrieve booking details (Flight, Hotel, PackageDeal)
        flight = Flight.query.get(flight_id) if flight_id else None
        hotel = Hotel.query.get(hotel_id) if hotel_id else None
        package_deal = PackageDeal.query.get(package_deal_id) if package_deal_id else None


        # Create a new reservation instance
        with BookingContext() as session:
            reservation = Reservation(
                user_id=user_id,
                package_deal_id=package_deal_id if package_deal_id else None,
                flight_id=flight_id if flight_id else None,
                hotel_id=hotel_id if hotel_id else None
            )

            db.session.add(reservation)
            db.session.commit()  # Commit here to save the reservation

        # Notify user by observer method
        booking_details = []
        if package_deal:
            booking_details.append(f"Package Deal: {package_deal.package_id} - Total Price: {package_deal.get_total_price()}$")

            if package_deal.flight:
                booking_details.append(f"Flight: {package_deal.flight.airline} from {package_deal.flight.from1} to {package_deal.flight.to} on {package_deal.flight.departure_time}")

            if package_deal.hotel:
                booking_details.append(f"Hotel: {package_deal.hotel.name} located at {package_deal.hotel.location}")

        else:
            if flight:
                booking_details.append(f"Flight: {flight.airline} from {flight.from1} to {flight.to} on {flight.departure_time}")
            if hotel:
                booking_details.append(f"Hotel: {hotel.name} located at {hotel.location}")


        message = f"Hello {reservation.user.username},\n\nYour booking has been successfully confirmed!\n\nReservation ID: {reservation.id}\n" + "\n".join(booking_details)     

        booking_subject = BookingSubject()
        email_notifier = EmailNotifier(current_user.email)
        booking_subject.attach(email_notifier)
        booking_subject.notify(message, current_user.email)

        flash("Reservation Successful", 'success')
        return redirect(url_for('user_dashboard', user_id=user_id))

    return render_template('add_reservation.html', title="Reservation")


# Cancle Reservation by user
@app.route('/cancel_reservation/<int:reservation_id>',methods=['POST','GET'])
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    
    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404
    
    # Optionally, you could change the status instead of deleting the record
    reservation.status = 'canceled'
    
    message = f"Hello {reservation.user.username},\n\nYour reservation has been successfully canceled!\n\n" \
              f"Reservation ID: {reservation.id}\n" \
              f"Status: {reservation.status}"
    
    email_notifier = EmailNotifier(current_user.email)
    booking_subject = BookingSubject()
    booking_subject.attach(email_notifier)
    booking_subject.notify(message, current_user.email)

    db.session.commit()
    flash("Reservation canceled successfully",'success'), 200
    return redirect(url_for('user_dashboard',user_id=reservation.user_id))


# _________________________________Reservation ends__________________________


# see all flight + search airlines
@app.route('/all_flights')
def all_flights():
    search_query = request.args.get('search', '')
    if search_query:
        flights = Flight.query.filter(Flight.airline.ilike(f'%{search_query}%')).all()
    else:
        flights = Flight.query.all()

    return render_template('user/all_flights.html',flights=flights,search_query=search_query,title="Flights")


# # see all hotel + search hotels
@app.route('/all_hotels')
def all_hotels():
    search_query = request.args.get('search', '')
    if search_query:
        hotel = Hotel.query.filter(Hotel.name.ilike(f'%{search_query}%')).all()
    else:
        hotel = Hotel.query.all()
    return render_template('user/all_hotels.html',hotel=hotel,title="Hotels")

# see all apckages
@app.route('/all_packages')
def all_packages():
    packages = PackageDeal.query.all()
    return render_template('user/all_packages.html',packages=packages,title="Packages")



# user dashboard 
@app.route('/user_dashboard/<int:user_id>', methods=['GET'])
@login_required
def user_dashboard(user_id):
    print(f"Entered user_dashboard for user_id: {user_id}")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    reservations = Reservation.query.filter_by(user_id=user.id).all()
    return render_template('user/user_dashboard.html', user=user, reservations=reservations, title="User Dashboard")




# ______________________________api________________________________________________________
# api to see all reservations
@app.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([
        {
            "id": r.id,
            "package_deal_id": r.package_deal_id,
            "flight_id": r.flight_id,
            "hotel_id": r.hotel_id,
            "reservation_date": r.reservation_date,
            "status": r.status
        } for r in reservations
    ]), 200



# api to see all reservations by id
@app.route('/reservations/<int:user_id>', methods=['GET'])
@login_required
def get_reservations_by_user(user_id):
    if user_id != current_user.id:
        return jsonify({"error": "Unauthorized access"}), 403

    # Query for all reservations for the specified user ID
    reservations = Reservation.query.filter_by(user_id=user_id).all()

    # If no reservations are found, return a message
    if not reservations:
        return jsonify({"error": "No reservations found for this user"}), 404

    # Create a list of reservation data
    reservations_data = []
    for reservation in reservations:
        reservations_data.append({
            "id": reservation.id,
            "package_deal_id": reservation.package_deal_id,
            "flight_id": reservation.flight_id,
            "hotel_id": reservation.hotel_id,
            "reservation_date": reservation.reservation_date,
            "status": reservation.status
        })

    return jsonify(reservations_data), 200



@app.route('/service', methods=['GET'])
def show_service_registry():
    # Get the list of registered services from the ServiceMeta metaclass
    registered_services = ServiceMeta.get_registered_services()
    
    # Create a list of service names (class names) from the registry
    services_data = [service.__name__ for service in registered_services]
    
    # Return the list as a JSON response
    return jsonify({
        "registered_services": services_data,
        "total_services_registered": len(services_data)
    })
