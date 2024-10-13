Overview:

A web application built with Flask to help manage travel plans, bookings, and itineraries efficiently.

_____________________________________set up__________________________
Getting Started:

Activate env:
path: . ev/bin/activate

Install all Packages 
path: pip install -r requirements.txt

Run task:
path:python3 app.py

if you want:
To Enable development mode
path: export FLASK_ENV=development

Set Environment variable to specify app:
path: export FLASK_APP=app.py
path: flask run or flask --app app.py --debug run

____________________________connect with database-postgresql______________________________
Connect with postgresql:

username: postgres
password:root
path: sudo apt install postgresql postgresql-contrib

Start and Enable PostgreSQL Service:
path: sudo systemctl start postgresql
path: sudo systemctl enable postgresql

Verify Installation:
path: sudo systemctl status postgresql

Access PostgreSQL:
sudo -i -u postgres
psql

path: CREATE DATABASE travel;

show Database: \l
connect to database: \c database_name
show tables: \dt
show user: \du
Exit: \q

*Requiured packages in flask:
pip install psycopg2
&
sudo apt install libpq-dev


________________________________connect with databse mysql______________________
username: root
password:root
sudo apt update
sudo apt install mariadb-server
sudo systemctl start mariadb
sudo mysql_secure_installation
(allow to all question and set password :root)


Access MySQL:
sudo mysql -u root -p
CREATE DATABSE travel;
USE travel;
SHOW tables 

connect with flask:

pip install pymysql
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

to install mysqlclient you need to install below packages:
sudo apt-get update
sudo apt-get install pkg-config
sudo apt-get install libmysqlclient-dev

install:
pip install mysqlclient

still its show error:
sudo mysql -u root -p
mariadb: SELECT user, host, plugin FROM mysql.user WHERE user = 'root';
mariadb: ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD('root');
FLUSH PRIVILEGES;
mariadb: GRANT ALL PRIVILEGES ON travel.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

then get started..



Features:
-Use Session for admin login and logout
-Use cookies to store user logging info
-Use Builder method to create packages(eg.flight+hotel)
-Use decorators to admin login ,Booking and Validate Booking Details
-Use Context Manager to handling Booking Sessions
-Use metaclass for service registry
-Use Middleware and Request Hooks for Managing request data of signin
-Use Observer method to notify user 
-Use Mail authentication to Update user for Reservation
-Search and book Flight,Hotel and Packages
-Admin panel for managing users and Manage Flights,Hotels and Packages
-Use Built in decoratores for user login 
-In models Use Inheritance,abstract method, class and static method, magic method.
-Use Forms for validate data
-apply Pagination in all pages which contains tables

URLs:

For Admin:
___________________

username:Admin
password:admin
__________________
http://127.0.0.1:5000/dashboard
http://127.0.0.1:5000/adminlogin
http://127.0.0.1:5000/adminlogout
http://127.0.0.1:5000/addflight
http://127.0.0.1:5000/showflight
http://127.0.0.1:5000/addhotel
http://127.0.0.1:5000/showhotel
http://127.0.0.1:5000/add_package
http://127.0.0.1:5000/show_packages
http://127.0.0.1:5000/show_reservation

for update and delete urls you can show in forentend side.

For User:
http://127.0.0.1:5000/
http://127.0.0.1:5000/register
http://127.0.0.1:5000/signin
http://127.0.0.1:5000/logout
http://127.0.0.1:5000/book # for reservation
http://127.0.0.1:5000/all_hotels (include search functionality)
http://127.0.0.1:5000/all_flights (include search functionality)
http://127.0.0.1:5000/all_packages (include search functionality)
http://127.0.0.1:5000/user_dashboard/user_id (show this url in navbar if user is logged)
http://127.0.0.1:5000/cancle_reservation/reservation_id

Note: After reservation user get notification of confirmation in mail.
after reservation you can show your reservation details in user_dashboard & you can also cancle your reservation

For Api:
http://127.0.0.1:5000/reservations
http://127.0.0.1:5000/reservations/user_id
http://127.0.0.1:5000/service (You can show all services by this url)
