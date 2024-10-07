from flask import Blueprint,render_template,session,request,flash,redirect,url_for
from Travel import app,db,bcrypt
from Travel.Admin.models import Admin,Flight,Hotel,PackageDeal
from Travel.Admin.forms import FlightForm,HotelForm,PackageDealForm
from Travel.decorators import admin_required
from Travel.Admin.Bulider import PackageBuilder
from Travel.User.models import Reservation,User

bp = Blueprint("admin",__name__)

# add 1 admin who can manage travel service
# admin = Admin(username='Admin', password=bcrypt.generate_password_hash('admin').decode('utf-8'))
# db.session.add(admin)
# db.session.commit()

# admin login
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username and password fields are filled
        if username == "" or password == "":
            flash('Please fill all the fields', 'danger')
            return redirect(url_for('adminlogin'))

        # Retrieve the admin by username
        admins = Admin.query.filter_by(username=username).first()
        
        # Ensure the admin exists and check the password
        if admins and bcrypt.check_password_hash(admins.password, password):
            session['admin_id'] = admins.id
            session['admin_name'] = admins.username
            flash('Login Successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Username or Password', 'danger')
            return redirect(url_for('adminlogin'))
    
    return render_template('admin/login.html', title="Admin")


# admin logout
@app.route('/adminlogout')
def adminlogout():
    if not session.get('admin_id'):
        return redirect('/adminlogin')
    if session.get('admin_id'):
        session['admin_id']=None
        session['admin_name']=None
        return redirect(url_for('adminlogin'))   

@app.route('/dashboard')
@admin_required
def dashboard():
    return render_template("admin/Dashboard.html",title="Admin")

# __________________________CRUD in Flight _______________________________________________

# create flight
@app.route('/addflight',methods=['GET','POST'])
@admin_required
def addflight():
    form = FlightForm()
    if form.validate_on_submit():
        try:
            flight = Flight(
                service_id=form.service_id.data,
                from1=form.from1.data,
                to=form.to.data,
                price=form.price.data,
                departure_time=form.departure_time.data,
                arrival_time=form.arrival_time.data,
                airline=form.airline.data,
                availability=form.availability.data
            )
            db.session.add(flight)
            db.session.commit()
            flash('Flight added successfully!','success')
            return redirect('showflight')
        except Exception as e:
            flash(f'An error occurred while adding the flight: {str(e)}', 'error')  # Catch any unexpected errors

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'error')  
    return render_template('admin/add_flight.html', form=form,title="Admin")


# show flight
@app.route('/showflight')
@admin_required
def showflight():
    flight = Flight.query.all()
    return render_template('admin/Showflights.html',flight=flight,title="Admin")

# update flight
@app.route('/update_flight/<int:flight_id>', methods=['GET', 'POST'])
def update_flight(flight_id):
    flight = Flight.query.get(flight_id)
    form = FlightForm(obj=flight)  # Pre-fill the form with flight data

    if form.validate_on_submit():
        try:
            flight.service_id = form.service_id.data
            flight.from1 = form.from1.data
            flight.to = form.to.data
            flight.price = form.price.data
            flight.departure_time = form.departure_time.data
            flight.arrival_time = form.arrival_time.data
            flight.airline = form.airline.data
            flight.availability = form.availability.data
            db.session.commit()
            flash('Flight updated successfully!', 'success')
            return redirect(url_for('showflight'))  # Redirect to a relevant page
        except Exception as e:
            flash(f'An error occurred while updating the flight: {str(e)}', 'error')

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'error') 

    return render_template('admin/add_flight.html', form=form, flight=flight,title="Admin")

# delete flight
@app.route('/delete_flight/<int:flight_id>',methods=['GET','POST'])
def delete_flight(flight_id):
    flight = Flight.query.get(flight_id)
    db.session.delete(flight)
    db.session.commit()
    return redirect(url_for('showflight'))
# _____________________________________end_____________________________________________

# ___________________________________CRUD in Hotel____________________________

# create hotel
@app.route('/addhotel',methods=['GET','POST'])
@admin_required
def addhotel():
    form = HotelForm()
    if form.validate_on_submit():
        try:
            hotel = Hotel(
                service_id=form.service_id.data,
                name=form.name.data,
                price=form.price.data,
                location=form.location.data,
                availability=form.availability.data
            )
            db.session.add(hotel)
            db.session.commit()
            flash('Hotel added successfully!','success')
            return redirect('showhotel')
        except Exception as e:
            flash(f'An error occurred while adding the hotel: {str(e)}', 'error') 

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'error')
    return render_template('admin/add_hotel.html', form=form,title='Admin')

# show hotels
@app.route('/showhotel')
@admin_required
def showhotel():
    hotel = Hotel.query.all()
    return render_template('admin/showhotels.html',hotel=hotel,title="Admin")

# update hotels
@app.route('/update_hotel/<int:hotel_id>', methods=['GET', 'POST'])
def update_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    form = HotelForm(obj=hotel)  # Pre-fill the form with flight data

    if form.validate_on_submit():
        try:
            hotel.service_id = form.service_id.data
            hotel.name = form.name.data
            hotel.price = form.price.data
            hotel.location = form.location.data
            hotel.availability = form.availability.data
            db.session.commit()
            flash('Hotel updated successfully!', 'success')
            return redirect(url_for('showhotel'))  # Redirect to a relevant page
        except Exception as e:
            flash(f'An error occurred while updating the hotel: {str(e)}', 'error')

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'error')
    return render_template('admin/add_hotel.html', form=form, hotel=hotel,title="Admin")

# delete hotels
@app.route('/delete_hotel/<int:hotel_id>',methods=['GET','POST'])
def delete_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    return redirect(url_for('show_packages'))


# __________________CRUD IN PACKAGE___________________________

# create package by builder method
@app.route('/add_package', methods=['GET', 'POST'])
@admin_required
def add_package():
    form = PackageDealForm()
    
    if form.validate_on_submit():
        flight = Flight.query.get(form.flight_id.data)
        hotel = Hotel.query.get(form.hotel_id.data)

        if flight and hotel:
            # Use PackageBuilder to create a new package
            package_builder = PackageBuilder()
            package = (package_builder
                       .add_flight(flight)
                       .add_hotel(hotel)
                       .set_package_id()
                       .build())

            # Set the package's availability based on the form
            package.availability = form.availability.data
            
            # Add the package to the database
            db.session.add(package)
            try:
                db.session.commit()
                flash('Package created successfully!', 'success')
                return redirect(url_for('show_packages'))
            except Exception as e:
                db.session.rollback()  # Rollback the session on error
                flash(f'An error occurred: {str(e)}', 'danger')
            

        flash('Flight or Hotel not found.', 'danger')

    # Fetch flights and hotels for the form
    flights = Flight.query.all()
    hotels = Hotel.query.all()
    return render_template('admin/add_package.html', form=form, flights=flights, hotels=hotels,title="Admin")

# show allpackages
@app.route('/show_packages')
@admin_required
def show_packages():
    packages = PackageDeal.query.all()
    return render_template('admin/show_packages.html', packages=packages,title="Admin")

# update packages
@app.route('/update_package/<int:package_id>', methods=['GET', 'POST'])
def update_package(package_id):
    package = PackageDeal.query.get_or_404(package_id)
    form = PackageDealForm()

    if form.validate_on_submit():
        flight = Flight.query.get(form.flight_id.data)
        hotel = Hotel.query.get(form.hotel_id.data)

        if flight and hotel:
            # Update the package details
            package.flight = flight
            package.hotel = hotel
            package.flight_id = flight.id
            package.hotel_id = hotel.id
            package.availability = form.availability.data

            # Commit the changes to the database
            try:
                db.session.commit()
                flash('Package updated successfully!', 'success')
                return redirect(url_for('show_packages'))  # Adjust to your view for showing packages
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'danger')
        else:
            flash('Flight or Hotel not found.', 'danger')

    # Populate the form with the current package data for editing
    form.flight_id.data = package.flight_id
    form.hotel_id.data = package.hotel_id
    form.availability.data = package.availability

    # Fetch flights and hotels for the dropdowns
    flights = Flight.query.all()
    hotels = Hotel.query.all()
    return render_template('admin/add_package.html', form=form, package=package, flights=flights, hotels=hotels,title="Admin")

# delete packages
@app.route('/delete_package/<int:package_id>', methods=['POST','GET'])
def delete_package(package_id):
    package = PackageDeal.query.get_or_404(package_id)
    db.session.delete(package)
    db.session.commit()
    flash('Package deleted successfully!', 'success')
    return redirect(url_for('show_packages'))

# show all reservations
@app.route('/show_reservation')
@admin_required
def show_reservation():
    reservations = Reservation.query.all()
    return render_template('admin/show_reservations.html',reservations=reservations,title="Admin")

# show users
@app.route('/show_user')
@admin_required
def show_user():
    users = User.query.all()
    return render_template('admin/show_user.html',users=users)